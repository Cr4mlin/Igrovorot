from django.urls import path
from posts import views

urlpatterns = [
    path('posts/', views.PostListView.as_view(), name='post_list'),
]
