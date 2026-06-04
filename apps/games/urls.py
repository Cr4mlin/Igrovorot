from django.urls import path
from games import views

urlpatterns = [
    path('games/', views.GameListView.as_view(), name='games'),
    path('steam/games/<int:app_id>/', views.SteamGameRedirectView.as_view(), name='steam_game_redirect'),
    path('games/<slug:slug>/', views.GameDetailView.as_view(), name='game_detail'),
    path('games/<slug:slug>/delete/', views.GameDeleteView.as_view(), name='game_delete'),
]
