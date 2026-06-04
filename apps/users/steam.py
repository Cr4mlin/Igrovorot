import re
import requests
from django.conf import settings

from games.models import Game
from games.steam import sync_steam_owned_games


def resolve_steam_id(steam_input):
    """
    Принимает любой формат — числовой ID или ссылку на профиль.
    Возвращает числовой Steam ID (строка) или None если не удалось.
    """
    if not steam_input:
        return None

    steam_input = steam_input.strip()

    if re.match(r'^\d{17}$', steam_input):
        return steam_input

    match = re.search(r'/profiles/(\d{17})', steam_input)
    if match:
        return match.group(1)

    match = re.search(r'/id/([^/]+)', steam_input)
    if match:
        username = match.group(1)
        return resolve_vanity_url(username)

    return resolve_vanity_url(steam_input)


def build_steam_profile_url(steam_input):
    if not steam_input:
        return ''

    steam_input = steam_input.strip()

    if steam_input.startswith(('http://', 'https://')):
        return steam_input

    match = re.search(r'/profiles/(\d{17})', steam_input)
    if match:
        return f"https://steamcommunity.com/profiles/{match.group(1)}/"

    match = re.search(r'/id/([^/]+)', steam_input)
    if match:
        return f"https://steamcommunity.com/id/{match.group(1).strip('/')}/"

    if re.match(r'^\d{17}$', steam_input):
        return f'https://steamcommunity.com/profiles/{steam_input}/'

    return f'https://steamcommunity.com/id/{steam_input.strip("/")}/'


def resolve_vanity_url(username):
    try:
        url = 'https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/'
        response = requests.get(url, params={
            'key': settings.STEAM_API_KEY,
            'vanityurl': username,
        }, timeout=5)
        data = response.json()
        if data.get('response', {}).get('success') == 1:
            return data['response']['steamid']
        return None
    except Exception:
        return None


def get_steam_games(steam_id):
    try:
        url = 'https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/'
        response = requests.get(url, params={
            'key': settings.STEAM_API_KEY,
            'steamid': steam_id,
            'include_appinfo': True,
            'include_played_free_games': True,
        }, timeout=5)
        data = response.json()
        games = data.get('response', {}).get('games', [])
        games.sort(key=lambda x: x.get('playtime_forever', 0), reverse=True)
        visible_games = games[:20]

        try:
            sync_steam_owned_games(visible_games)
        except Exception:
            pass

        game_slugs = {
            game.steam_app_id: game.slug
            for game in Game.objects.filter(
                steam_app_id__in=[game.get('appid') for game in visible_games if game.get('appid')]
            )
        }

        result = []
        for game in visible_games:
            playtime = game.get('playtime_forever', 0)
            app_id = game.get('appid')
            result.append({
                'name': game.get('name', ''),
                'appid': app_id,
                'game_slug': game_slugs.get(app_id),
                'playtime_hours': round(playtime / 60, 1),
                'cover_url': f'https://cdn.akamai.steamstatic.com/steam/apps/{app_id}/header.jpg',
                'icon_url': f"https://media.steampowered.com/steamcommunity/public/images/apps/{game['appid']}/{game.get('img_icon_url', '')}.jpg" if game.get(
                    'img_icon_url') else None,
            })
        return result

    except Exception:
        return []
