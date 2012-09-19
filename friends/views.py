from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required

from friends.models import Friendship


class UserFriendsListView(ListView):
    context_object_name = "user_friends"
    template_name = "friends/friend_list.html"

    def get_queryset(self):
        return Friendship.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(UserFriendsListView, self).get_context_data(**kwargs)
        error = self.request.REQUEST.get('error', None)
        if error:
            context['error'] = error
        return context
    
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


@login_required
def add_friend(request):
    if request.method == 'POST':
        username = request.POST['username']
        try:
            friend = User.objects.get(username=username)
        except User.DoesNotExist:
            return redirect("/friends/?error=no_friend")
        Friendship.create_friendship(request.user, friend)
        return redirect("/friends/")
