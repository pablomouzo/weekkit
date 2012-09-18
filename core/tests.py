import json
import datetime

from django.contrib.auth.models import User

from django.test import TestCase


class BaseApiTest(TestCase):
    def get_json(self, url, status_code):
        response = self.client.get(url)
        self.assertEqual(response.status_code, status_code,
                         response.content)
        response_json = json.loads(response.content)
        return response_json


class ProxyApiTest(BaseApiTest):
    def setUp(self):
        user = User.objects.create_user('johndoe',
                                        'john@doe.com',
                                        'johndoe')
        self.client.login(username='johndoe', password='johndoe')
    
    def test_simple_get(self):
        "Just make sure the basic logic for the proxy is in place"
        response = self.client.get('/reddit_proxy/search.json',
                                   {'q': 'arg'},
                                   follow=True)

        self.assertEquals(response.status_code, 200)


class AddSubredditViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('johndoe',
                                             'john@doe.com',
                                             'johndoe')
        self.client.login(username='johndoe', password='johndoe')
    
    def test_add_subreddit_ajax(self):
        response = self.client.post("/add_subreddit/",
                                    {'name': "testsubreddit"},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertEquals(response.status_code, 201)
        # FIX: use assert not raise
        self.user.subreddits.get(name="testsubreddit")
