from django.db import models
from django.contrib.auth.models import User


class Friendship(models.Model):
    """ A user's friendship

    A complete friendship is represented by two of these objects
    """
    user = models.ForeignKey(User, related_name="friendships")
    friend = models.ForeignKey(User, related_name="+")

    class Meta:
        unique_together = (('user', 'friend'),)

    @classmethod
    def create_friendship(cls, user1, user2):
        """ Create a friendship between two users """
        cls(user=user1, friend=user2).save()
        cls(user=user2, friend=user1).save()

    def __unicode__(self):
        return str(self.friend)


class FriendRequest(models.Model):
    """ A friend request

    A user sends a friend request to other user to
    create a frienship.

    rfrom: user that initiated the request
    rto: user that received the request
    """
    rfrom = models.ForeignKey(User, related_name="friend_requests_received")
    rto = models.ForeignKey(User, related_name="friend_requests_made")

    def __unicode__(self):
        return "From %s to %s" % (str(self.rfrom), str(self.rto))
