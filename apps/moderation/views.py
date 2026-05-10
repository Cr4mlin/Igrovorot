from collections import defaultdict
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.views import View
from users.mixins import ModeratorRequiredMixin
from users.models import User
from posts.models import Post
from reviews.models import Review
from moderation.models import Report
from moderation.forms import ReportForm


class ModerationView(ModeratorRequiredMixin, View):
    template_name = 'moderation/moderation.html'

    def get(self, request):
        posts = list(Post.objects.select_related('author').order_by('-created_at'))
        reviews = list(Review.objects.select_related('author', 'game').order_by('-created_at'))
        users = list(User.objects.order_by('-date_joined'))

        post_ct = ContentType.objects.get_for_model(Post)
        review_ct = ContentType.objects.get_for_model(Review)
        user_ct = ContentType.objects.get_for_model(User)

        open_reports = Report.objects.filter(is_resolved=False).select_related('user')
        reports_map = defaultdict(list)
        for report in open_reports:
            reports_map[(report.content_type_id, report.object_id)].append(report)

        for post in posts:
            post.open_reports = reports_map.get((post_ct.id, post.pk), [])
        for review in reviews:
            review.open_reports = reports_map.get((review_ct.id, review.pk), [])
        for user in users:
            user.open_reports = reports_map.get((user_ct.id, user.pk), [])

        return render(request, self.template_name, {
            'posts': posts,
            'reviews': reviews,
            'users': users,
        })


class ReportCreateView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def post(self, request, app_label, model_name, object_id):
        content_type = get_object_or_404(ContentType, app_label=app_label, model=model_name)

        if Report.objects.filter(user=request.user, content_type=content_type, object_id=object_id).exists():
            return redirect(request.META.get('HTTP_REFERER', '/'))

        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.content_type = content_type
            report.object_id = object_id
            report.created_at = timezone.now()
            report.save()

        return redirect(request.META.get('HTTP_REFERER', '/'))


class ReportResolveView(ModeratorRequiredMixin, View):

    def post(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        report.is_resolved = True
        report.save()
        return redirect('moderation')
