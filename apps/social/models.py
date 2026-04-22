from django.db import models

class Follow(models.Model):
    follower = models.ForeignKey('User', models.DO_NOTHING)
    following = models.ForeignKey('User', models.DO_NOTHING, related_name='follow_following_set')
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'follow'
        unique_together = (('follower', 'following'),)


class Like(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING)
    post = models.ForeignKey('Post', models.DO_NOTHING, blank=True, null=True)
    review = models.ForeignKey('Review', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'like'
        unique_together = (('user', 'post'), ('user', 'review'),)
