from django.urls import path
from social import views

urlpatterns = [
    path('social/like/', views.LikeView.as_view(), name='like'),
]
