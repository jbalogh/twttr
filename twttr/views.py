from django.shortcuts import render, get_object_or_404

from .models import User, Tweet


def home(request):
    tweets = Tweet.objects.order_by('-created')[:30]
    return render(request, 'twttr/base.html', {'tweets': tweets})


def user(request, username):
    tweets = (Tweet.objects.filter(user__screen_name=username)
              .order_by('-created'))[:30]
    return render(request, 'twttr/base.html', {'tweets': tweets})


def tweet(request, username, id):
    tweet = get_object_or_404(Tweet, user__screen_name=username, id=id)
    return render(request, 'twttr/base.html', {'tweets': [tweet]})


def timeline(request, username):
    tweets = (Tweet.objects.filter(user__friends__screen_name=username)
              .order_by('-created'))[:30]
    return render(request, 'twttr/base.html', {'tweets': tweets})
