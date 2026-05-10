from django.shortcuts import render
from django.views import View
from users.mixins import ModeratorRequiredMixin
from users.models import User
from posts.models import Post
from reviews.models import Review


class ModerationView(ModeratorRequiredMixin, View):
    template_name = 'moderation/moderation.html'

    def get(self, request):
        posts = Post.objects.select_related('author').order_by('-created_at')
        reviews = Review.objects.select_related('author', 'game').order_by('-created_at')
        users = User.objects.order_by('-date_joined')
        return render(request, self.template_name, {
            'posts': posts,
            'reviews': reviews,
            'users': users,
        })
