from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.contrib.auth.decorators import login_required

from core.models import UserSubreddit

import requests

@login_required
def index(request):
    return render_to_response("core/index.html",
                              {'user_subreddits': request.user.usersubreddit_set.all()},
                              context_instance=RequestContext(request))


@login_required
def add_subreddit(request):
    user = request.user
    if request.method == 'POST':
        name = request.POST['name']
        us = UserSubreddit(user=user, name=name)
        us.save()
        return HttpResponse("", status=201)


@login_required
def reddit_proxy(request):
    url = "http://www.reddit.com" + request.path[13:]
    if request.method == 'GET':
        r = requests.get(url, params=request.GET)
    elif request.method == 'POST':
        raise NotImplementedError()
    return HttpResponse(r.text,
                        status=r.status_code,
                        mimetype=r.headers['content-type'])
