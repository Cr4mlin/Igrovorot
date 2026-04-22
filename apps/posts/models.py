from django.db import models
from django.conf import settings


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.CharField(max_length=512, blank=True, null=True)
    tags = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_published = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'post'


class Comment(models.Model):
    post = models.ForeignKey('Post', models.DO_NOTHING)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING)
    content = models.TextField()
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'comment'