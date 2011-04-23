from django.conf.urls.defaults import url

from . import views


urlpatterns = (
    url('^$', views.home),
    url('^post/(?P<username>[^/]+)?$', views.post, name='twttr.post'),
    url('^(?P<username>[^/]+)/$', views.user, name='twttr.user'),
    url('^(?P<username>[^/]+)/timeline$',
        views.timeline, name='twttr.timeline'),
    url('^(?P<username>[^/]+)/(?P<id>\w+)$', views.tweet, name='twttr.tweet'),
)
