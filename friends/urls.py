from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from friends.views import UserFriendsListView, UserFriendSubredditsView


urlpatterns = patterns('friends.views',
    url(r'^$', login_required(UserFriendsListView.as_view())),
    url(r'^(\w+)/$', UserFriendSubredditsView.as_view())                       
)
