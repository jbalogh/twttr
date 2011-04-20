from django.shortcuts import render, get_object_or_404

from .models import User, Tweet


def home(request):
    tweets = Tweet.objects.order_by('-created')[:20]
    return render(request, 'twttr/base.html', {'tweets': tweets})


def user(request, username):
    user = get_object_or_404(User, screen_name=username)
    tweets = Tweet.objects.filter(user=user).order_by('-created')[:20]
    return render(request, 'twttr/base.html', {'tweets': tweets})


def tweet(request, username, id):
    user = get_object_or_404(User, screen_name=username)
    tweet = get_object_or_404(Tweet, user=user, id=id)
    return render(request, 'twttr/base.html', {'tweets': [tweet]})
