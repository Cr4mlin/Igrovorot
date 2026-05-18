from django.urls import path
from django.views.decorators.cache import cache_page
from games import views

urlpatterns = [
    path('games/', cache_page(60 * 15)(views.GameListView.as_view()), name='games'),
    path('games/<slug:slug>/', views.GameDetailView.as_view(), name='game_detail'),
    path('games/<slug:slug>/delete/', views.GameDeleteView.as_view(), name='game_delete'),
]