from django.db import models


class Profile(models.Model):
    user = models.OneToOneField('User', models.DO_NOTHING)
    avatar = models.CharField(max_length=512, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    steam_id = models.CharField(max_length=100, blank=True, null=True)
    is_banned = models.BooleanField()
    banned_until = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'profile'


class User(models.Model):
    username = models.CharField(unique=True, max_length=150)
    email = models.CharField(unique=True, max_length=254)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user'


class UserGameList(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    game = models.ForeignKey('Game', models.DO_NOTHING)
    status = models.CharField(max_length=50)
    hours_played = models.DecimalField(max_digits=8, decimal_places=2)
    added_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user_game_list'
        unique_together = (('user', 'game'),)