from django.db import models
from django.contrib.auth.models import User


class Friend(models.Model):
    """ A user's friend

    A friendship is represented by two of these objects
    """
    user = models.ForeignKey(User, related_name="friends")
    friend = models.ForeignKey(User, related_name="+")

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
