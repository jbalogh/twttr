from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('',
    url('', include('twttr.urls')),
)
