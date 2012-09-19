from django.contrib.auth.models import User

from django.test import TestCase

from friends.models import Friendship

class FriendsSubredditsViewTest(TestCase):
    def setUp(self):
        user1 = User.objects.create_user('johndoe',
                                         'john@doe.com',
                                         'johndoe')
        self.client.login(username='johndoe', password='johndoe')

        user2 = User.objects.create_user('janedoe',
                                         'jane@doe.com',
                                         'janedoe')

        Friendship.create_friendship(user1, user2)

    def test_void(self):
        pass
