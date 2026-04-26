from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views import View
from django.core.paginator import Paginator
from django.utils import timezone
from posts.models import Post
from posts.forms import PostForm, CommentForm


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
        can_edit = request.user.is_authenticated and (
            post.author == request.user or
            request.user.groups.filter(name='Moderator').exists()
        )
        return render(request, self.template_name, {
            'post': post,
            'comments': comments,
            'form': form,
            'can_edit': can_edit,
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


class PostCreateView(LoginRequiredMixin, View):
    template_name = 'posts/post_create.html'
    login_url = '/accounts/login/'

    def get(self, request):
        form = PostForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.created_at = timezone.now()
            post.updated_at = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
        return render(request, self.template_name, {'form': form})


class PostEditView(LoginRequiredMixin, View):
    template_name = 'posts/post_edit.html'
    login_url = '/accounts/login/'

    def _get_post_or_403(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        is_moderator = request.user.groups.filter(name='Moderator').exists()
        if post.author != request.user and not is_moderator:
            raise PermissionDenied
        return post

    def get(self, request, pk):
        post = self._get_post_or_403(request, pk)
        form = PostForm(instance=post)
        return render(request, self.template_name, {'form': form, 'post': post})

    def post(self, request, pk):
        post = self._get_post_or_403(request, pk)
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            edited_post = form.save(commit=False)
            edited_post.updated_at = timezone.now()
            edited_post.save()
            return redirect('post_detail', pk=post.pk)
        return render(request, self.template_name, {'form': form, 'post': post})


class PostDeleteView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def _get_post_or_403(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        is_moderator = request.user.groups.filter(name='Moderator').exists()
        if post.author != request.user and not is_moderator:
            raise PermissionDenied
        return post

    def get(self, request, pk):
        post = self._get_post_or_403(request, pk)
        return render(request, 'posts/post_confirm_delete.html', {'post': post})

    def post(self, request, pk):
        post = self._get_post_or_403(request, pk)
        post.delete()
        return redirect('post_list')


class FeedView(View):
    template_name = 'posts/feed.html'
    paginate_by = 10

    def get(self, request):
        posts = Post.objects.filter(is_published=True).order_by('-created_at')
        paginator = Paginator(posts, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {'page_obj': page_obj})
