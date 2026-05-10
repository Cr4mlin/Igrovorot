from django.urls import path
from moderation import views

urlpatterns = [
    path('moderation/', views.ModerationView.as_view(), name='moderation'),
]
