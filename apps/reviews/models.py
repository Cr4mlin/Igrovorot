from django.db import models
from django.conf import settings

class Review(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING)
    game = models.ForeignKey('games.Game', models.DO_NOTHING)
    rating = models.SmallIntegerField()
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'review'
        unique_together = (('author', 'game'),)
