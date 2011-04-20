from django.conf.urls.defaults import url

from . import views


urlpatterns = (
    url('^$', views.home),
    url('^(?P<username>[^/]+)/$', views.user, name='twttr.user'),
    url('^(?P<username>[^/]+)/(?P<id>\w+)$', views.tweet, name='twttr.tweet'),
)
