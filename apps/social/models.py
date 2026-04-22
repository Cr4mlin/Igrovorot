from django.db import models
from django.conf import settings

class Follow(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING)
    following = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, related_name='follow_following_set')
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'follow'
        unique_together = (('follower', 'following'),)


class Like(models.Model):
    user = models.ForeignKey('users.User', models.DO_NOTHING)
    post = models.ForeignKey('posts.Post', models.DO_NOTHING, blank=True, null=True)
    review = models.ForeignKey('reviews.Review', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'like'
        unique_together = (('user', 'post'), ('user', 'review'),)
