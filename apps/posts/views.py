from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.core.paginator import Paginator
from posts.models import Post
from posts.forms import CommentForm


class PostListView(View):
    template_name = 'posts/post_list.html'
    paginate_by = 10

    def get(self, request):
        posts = Post.objects.filter(is_published=True).order_by('-created_at')
        paginator = Paginator(posts, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {'page_obj': page_obj})


class PostDetailView(View):
    template_name = 'posts/post_detail.html'

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk, is_published=True)
        comments = post.comment_set.select_related('author').order_by('created_at')
        form = CommentForm()
        return render(request, self.template_name, {
            'post': post,
            'comments': comments,
            'form': form,
        })

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk, is_published=True)
        if not request.user.is_authenticated:
            return redirect('login')
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=pk)
        comments = post.comment_set.select_related('author').order_by('created_at')
        return render(request, self.template_name, {
            'post': post,
            'comments': comments,
            'form': form,
        })


class FeedView(View):
    template_name = 'posts/feed.html'
    paginate_by = 10

    def get(self, request):
        posts = Post.objects.filter(is_published=True).order_by('-created_at')
        paginator = Paginator(posts, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {'page_obj': page_obj})
