import uuid

from django.shortcuts import render, get_object_or_404, redirect

from .models import User, Tweet


def home(request):
    tweets = Tweet.objects.order_by('-created').select_related('user')[:30]
    return render(request, 'twttr/base.html', {'tweets': tweets})


def user(request, username):
    user_ = User.objects.get(screen_name=username)
    tweets = (Tweet.objects.filter(user=user_).select_related('user').order_by('-created'))[:30]
    return render(request, 'twttr/base.html', {'tweets': tweets})


def tweet(request, username, id):
    tweet = get_object_or_404(Tweet, user__screen_name=username, id=id)
    return render(request, 'twttr/base.html', {'tweets': [tweet]})


def timeline(request, username):
    tweets = (Tweet.objects.filter(user__friends__screen_name=username)
              .order_by('-created'))[:30]
    return render(request, 'twttr/base.html', {'tweets': tweets})


def post(request, username=None):
    username = username or 'BieberShawties'
    if request.method == 'POST' and 'tweet' in request.POST:
        user = get_object_or_404(User, screen_name=username)
        Tweet.objects.create(user=user, text=request.POST['tweet'],
                             source='web', id=uuid.uuid4().hex)
        return redirect('twttr.user', username)
    return render(request, 'twttr/post.html', {'username': username})
