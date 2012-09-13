from django.db import models
from django.contrib.auth.models import User


class UserSubreddit(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=200)

    class Meta:
        unique_together = (('user', 'name',))

    def __unicode__(self):
        return "%s - %s" % (self.user, self.name)
