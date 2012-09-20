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


class AddFriendViewTest(TestCase):
    def setUp(self):
        user1 = User.objects.create_user('johndoe',
                                         'john@doe.com',
                                         'johndoe')
        self.client.login(username='johndoe', password='johndoe')
        self.user = user1

        user2 = User.objects.create_user('janedoe',
                                         'jane@doe.com',
                                         'janedoe')

    def test_add_friend(self):
        """ Should add the friend and redirect to /friends/ """
        response = self.client.post("/friends/add_friend/",
                                    {'username': 'janedoe'})

        print response.status_code
        self.assertRedirects(response, "/friends/")
        print self.user.friendships.all()
        try:
            self.user.friendships.get(friend__username="janedoe")
        except:
            self.fail("Friend wasn't added")

    def test_add_non_existant_friend(self):
        """ Should fail and redirect with an error """
        friends_count = self.user.friendships.count()

        response = self.client.post("/friends/add_friend/",
                                    {'username': 'notexistant'})

        self.assertRedirects(response, "/friends/?error=no_friend")
        self.assertEquals(friends_count, self.user.friendships.count())
