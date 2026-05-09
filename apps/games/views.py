from django.shortcuts import render, get_object_or_404
from django.views import View
from django.core.paginator import Paginator
from games.models import Game, Genre


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

        return render(request, self.template_name, {
            'game': game,
            'genres': genres,
        })