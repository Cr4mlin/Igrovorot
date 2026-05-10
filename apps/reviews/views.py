from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views import View
from games.models import Game
from reviews.models import Review
from reviews.forms import ReviewForm


class ReviewCreateView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def post(self, request, slug):
        game = get_object_or_404(Game, slug=slug)

        if Review.objects.filter(author=request.user, game=game).exists():
            return redirect('game_detail', slug=slug)

        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.game = game
            review.created_at = timezone.now()
            review.updated_at = timezone.now()
            review.save()

        return redirect('game_detail', slug=slug)
