from django.conf.urls import patterns, include, url

urlpatterns = patterns('core.views',
    url(r'^$', 'index'),
    url(r'^add_subreddit/$', 'add_subreddit'),
    url(r'^reddit_proxy/', 'reddit_proxy')
)
