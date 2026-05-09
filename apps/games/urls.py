from django.urls import path
from games import views

urlpatterns = [
    path('games/', views.GameListView.as_view(), name='games'),
    path('games/<slug:slug>/', views.GameDetailView.as_view(), name='game_detail'),
]