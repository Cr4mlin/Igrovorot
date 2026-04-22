from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='media/avatars/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    steam_id = models.CharField(max_length=100, blank=True, null=True)
    is_banned = models.BooleanField(default=False)
    banned_until = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'profile'

    def __str__(self):
        return f'Профиль {self.user.username}'


class User(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'  # вход по email
    REQUIRED_FIELDS = ['username']  # username всё ещё обязателен

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.email


class UserGameList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING)
    game = models.ForeignKey('games.Game', models.DO_NOTHING)
    status = models.CharField(max_length=50)
    hours_played = models.DecimalField(max_digits=8, decimal_places=2)
    added_at = models.DateTimeField()

    class Meta:
        db_table = 'user_game_list'
        unique_together = (('user', 'game'),)