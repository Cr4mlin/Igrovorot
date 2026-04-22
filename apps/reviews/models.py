from django.db import models

class Review(models.Model):
    author = models.ForeignKey('users.User', models.DO_NOTHING)
    game = models.ForeignKey('games.Game', models.DO_NOTHING)
    rating = models.SmallIntegerField()
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'review'
        unique_together = (('author', 'game'),)
