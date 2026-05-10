from django.shortcuts import render, get_object_or_404
from django.views import View
from django.core.paginator import Paginator
from games.models import Game, Genre
from games.steam import get_steam_game_details
from reviews.models import Review
from reviews.forms import ReviewForm


class GameListView(View):
    template_name = 'games/game_list.html'

    def get(self, request):
        games = Game.objects.all().order_by('title')
        genres = Genre.objects.all().order_by('name')

        # Фильтрация по жанру
        genre_slug = request.GET.get('genre')
        if genre_slug:
            games = games.filter(gamegenre__genre__slug=genre_slug)

        # Поиск по названию
        query = request.GET.get('q')
        if query:
            games = games.filter(title__icontains=query)

        paginator = Paginator(games, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, self.template_name, {
            'page_obj': page_obj,
            'genres': genres,
            'selected_genre': genre_slug,
            'query': query or '',
        })


class GameDetailView(View):
    template_name = 'games/game_detail.html'

    def get(self, request, slug):
        game = get_object_or_404(Game, slug=slug)
        genres = game.gamegenre_set.select_related('genre').all()

        # Подтягиваем данные из Steam если есть app_id
        steam_data = None
        if game.steam_app_id:
            steam_data = get_steam_game_details(game.steam_app_id)

        user_review = None
        review_form = None
        if request.user.is_authenticated:
            user_review = Review.objects.filter(author=request.user, game=game).first()
            if not user_review:
                review_form = ReviewForm()

        reviews = Review.objects.filter(game=game).select_related('author').order_by('-created_at')

        return render(request, self.template_name, {
            'game': game,
            'genres': genres,
            'steam_data': steam_data,
            'review_form': review_form,
            'user_review': user_review,
            'reviews': reviews,
        })