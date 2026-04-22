from django.db import models


class Post(models.Model):
    author = models.ForeignKey('users.User', models.DO_NOTHING)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.CharField(max_length=512, blank=True, null=True)
    tags = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_published = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'post'


class Comment(models.Model):
    post = models.ForeignKey('Post', models.DO_NOTHING)
    author = models.ForeignKey('users.User', models.DO_NOTHING)
    content = models.TextField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'comment'