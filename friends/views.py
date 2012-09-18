from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User

from friends.models import Friendship


class UserFriendsListView(ListView):
    context_object_name = "user_friends"
    template_name = "friends/friend_list.html"

    def get_queryset(self):
        return Friendship.objects.filter(user=self.request.user)


class UserFriendSubredditsView(DetailView):
    context_object_name = "friend"
    template_name = "friends/friend_subreddit_list.html"

    def get_object(self):
        # Find user
        friend = get_object_or_404(User, username=self.args[0])
        
        # Check that users are friends
        get_object_or_404(Friendship,
                          user=self.request.user,
                          friend=friend)
        return friend
