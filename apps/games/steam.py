import re

import requests
from django.core.cache import cache
from django.utils.text import slugify

from games.models import Game, GameGenre, Genre


def clean_requirement_heading(requirements):
    """Убирает служебный заголовок Steam из начала HTML требований."""
    if not requirements:
        return ''

    patterns = [
        r'^\s*<strong>\s*(?:minimum|recommended|минимальные|рекомендованные)(?:\s+requirements?)?\s*:?\s*</strong>\s*',
        r'^\s*(?:minimum|recommended|минимальные|рекомендованные)(?:\s+requirements?)?\s*:?\s*',
    ]

    cleaned = requirements
    for pattern in patterns:
        cleaned = re.sub(pattern, '', cleaned, count=1, flags=re.IGNORECASE)

    return cleaned


def make_unique_game_slug(title, app_id):
    base_slug = slugify(title) or f'game-{app_id}'
    slug = base_slug
    counter = 1

    while Game.objects.filter(slug=slug).exists():
        slug = f'{base_slug}-{counter}'
        counter += 1

    return slug


def create_steam_game(app_id, fallback_title=''):
    game = Game.objects.filter(steam_app_id=app_id).first()
    if game:
        return game

    details = get_steam_game_details(app_id)
    if not details and not fallback_title:
        return None

    title = (details or {}).get('title') or fallback_title or f'Steam App {app_id}'
    genres = (details or {}).get('genres') or []

    game = Game.objects.create(
        title=title,
        slug=make_unique_game_slug(title, app_id),
        description=(details or {}).get('short_description') or None,
        cover=f'https://cdn.akamai.steamstatic.com/steam/apps/{app_id}/header.jpg',
        developer=((details or {}).get('developers') or [None])[0],
        steam_app_id=app_id,
    )

    for genre_name in genres:
        genre_slug = slugify(genre_name) or f'genre-{genre_name}'
        genre, _ = Genre.objects.get_or_create(
            slug=genre_slug,
            defaults={'name': genre_name},
        )
        GameGenre.objects.get_or_create(game=game, genre=genre)

    cache.set('games_list_version', cache.get('games_list_version', 0) + 1)
    return game


def sync_steam_owned_games(owned_games, limit=3):
    """
    Добавляет в каталог отсутствующие игры из Steam-библиотеки пользователя.
    Ограничение нужно, чтобы открытие профиля не делало десятки Steam API запросов.
    """
    created = 0

    for owned_game in owned_games:
        if created >= limit:
            break

        app_id = owned_game.get('appid')
        title = (owned_game.get('name') or '').strip()
        if not app_id or not title:
            continue

        if Game.objects.filter(steam_app_id=app_id).exists():
            continue

        if create_steam_game(app_id, fallback_title=title):
            created += 1

    return created


def search_steam_app_id(title):
    """Ищет игру в Steam по названию, возвращает app_id или None."""
    try:
        url = 'https://store.steampowered.com/api/storesearch/'
        response = requests.get(url, params={
            'term': title,
            'l': 'russian',
            'cc': 'RU',
        }, timeout=5)
        data = response.json()
        items = data.get('items', [])
        if items:
            return items[0]['id']
        return None
    except Exception:
        return None


def get_steam_game_details(app_id):
    """Получает детальную информацию об игре из Steam Store."""
    try:
        url = f'https://store.steampowered.com/api/appdetails'
        response = requests.get(url, params={
            'appids': app_id,
            'l': 'russian',
        }, timeout=5)
        data = response.json()
        game_data = data.get(str(app_id), {})

        if not game_data.get('success'):
            return None

        details = game_data['data']

        screenshots = [
            s['path_full'] for s in details.get('screenshots', [])[:6]
        ]

        trailers = []
        for movie in details.get('movies', [])[:2]:
            movie_mp4 = movie.get('mp4', {})
            movie_webm = movie.get('webm', {})
            trailer_url = movie_mp4.get('max') or movie_mp4.get('480', '')
            trailer_type = 'video/mp4' if trailer_url else ''

            if not trailer_url:
                trailer_url = movie_webm.get('max') or movie_webm.get('480', '')
                trailer_type = 'video/webm' if trailer_url else ''

            if not trailer_url:
                trailer_url = movie.get('hls_h264', '')
                trailer_type = 'application/vnd.apple.mpegurl' if trailer_url else ''

            if trailer_url:
                trailers.append({
                    'name': movie.get('name', 'Трейлер'),
                    'url': trailer_url,
                    'type': trailer_type,
                    'thumb': movie.get('thumbnail', ''),
                })

        trailer = trailers[0] if trailers else {}

        metacritic = details.get('metacritic', {})

        pc_requirements = details.get('pc_requirements', {})

        return {
            'steam_url': f'https://store.steampowered.com/app/{app_id}/',
            'title': details.get('name', ''),
            'short_description': details.get('short_description', ''),
            'detailed_description': details.get('detailed_description', ''),
            'screenshots': screenshots,
            'trailers': trailers,
            'trailer_url': trailer.get('url', ''),
            'trailer_type': trailer.get('type', ''),
            'trailer_thumb': trailer.get('thumb', ''),
            'metacritic_score': metacritic.get('score'),
            'metacritic_url': metacritic.get('url'),
            'recommendations': details.get('recommendations', {}).get('total'),
            'header_image': details.get('header_image', ''),
            'developers': details.get('developers', []),
            'publishers': details.get('publishers', []),
            'genres': [g['description'] for g in details.get('genres', [])],
            'requirements_minimum': clean_requirement_heading(pc_requirements.get('minimum', '')),
            'requirements_recommended': clean_requirement_heading(pc_requirements.get('recommended', '')),
        }
    except Exception:
        return None
