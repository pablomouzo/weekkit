import json

from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from django.contrib.auth.decorators import login_required

from core.models import UserSubreddit

import requests

import praw


@login_required
def index(request):
    return render_to_response("core/index.html",
                              {'user_subreddits': request.user.subreddits.all()},
                              context_instance=RequestContext(request))


@login_required
def add_subreddit(request):
    user = request.user
    if request.method == 'POST':
        name = request.POST['name']
        us = UserSubreddit(user=user, name=name)
        us.save()
        if request.is_ajax():
            return HttpResponse("", status=201)
        else:
            return redirect(request.META['HTTP_REFERER'])


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


@login_required
def search_subreddit_names(request):
    r = praw.Reddit(user_agent="weekkit")
    subreddits = r.search_reddit_names(request.GET['query'])
    names = [{'name': sr.display_name} for sr in subreddits]
    return HttpResponse(json.dumps(names),
                        mimetype="application/json")
