from django.contrib.auth.models import User

from django.test import TestCase


class FriendsSubredditsViewTest(TestCase):
    def setUp(self):
        user1 = User.objects.create_user('johndoe',
                                         'john@doe.com',
                                         'johndoe')
        self.client.login(username='johndoe', password='johndoe')

        user2 = User.objects.create_user('janedoe',
                                         'jane@doe.com',
                                         'janedoe')
