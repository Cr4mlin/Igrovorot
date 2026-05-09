from django.http import JsonResponse
from django.views import View
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from social.models import Like
from posts.models import Post


@method_decorator(require_POST, name='dispatch')
class LikeView(View):

    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Unauthorized'}, status=401)

        post_id = request.POST.get('post_id')
        if not post_id:
            return JsonResponse({'error': 'Необходимо передать post_id'}, status=400)

        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return JsonResponse({'error': 'Пост не найден'}, status=404)

        like = Like.objects.filter(user=request.user, post=post, review=None).first()
        if like:
            like.delete()
            liked = False
        else:
            Like.objects.create(user=request.user, post=post, review=None, created_at=timezone.now())
            liked = True

        count = Like.objects.filter(post=post, review=None).count()
        return JsonResponse({'liked': liked, 'count': count})
