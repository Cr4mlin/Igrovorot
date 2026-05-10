from django.urls import path
from reviews import views

urlpatterns = [
    path('games/<slug:slug>/review/', views.ReviewCreateView.as_view(), name='review_create'),
]
