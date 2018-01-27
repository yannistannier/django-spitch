from django.db import models
from apps.authentication.models import User


class Follow(models.Model):
    user = models.ForeignKey(User, related_name="follows")
    follow = models.ForeignKey(User, related_name="followers")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'follow')


class FacebookFriend(models.Model):
    user = models.ForeignKey(User, related_name="facebook_friends")
    friend = models.ForeignKey(User)
    # follow = models.BooleanField(default=False)

    def __str__(self):
        return '{} - {}'.format(self.user, self.friend)


