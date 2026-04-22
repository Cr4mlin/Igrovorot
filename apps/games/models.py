from django.db import models

class Game(models.Model):
    title = models.CharField(max_length=255)
    slug = models.CharField(unique=True, max_length=280)
    description = models.TextField(blank=True, null=True)
    cover = models.CharField(max_length=512, blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    developer = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'game'


class GameGenre(models.Model):
    pk = models.CompositePrimaryKey('game_id', 'genre_id')
    game = models.ForeignKey(Game, models.DO_NOTHING)
    genre = models.ForeignKey('Genre', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'game_genre'


class Genre(models.Model):
    name = models.CharField(unique=True, max_length=100)
    slug = models.CharField(unique=True, max_length=120)

    class Meta:
        managed = False
        db_table = 'genre'
