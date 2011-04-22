import time

from django.core.urlresolvers import resolve

from statsd import statsd


class StatsdMiddleware:

    def process_request(self, request):
        request._start = time.time()
        request._name = resolve(request.path).url_name

    def process_response(self, request, response):
        statsd.incr('http.200')
        statsd.timing(request._name,
                      int(1000 * (time.time() - request._start)))
        return response

    def process_exception(self, request, exc):
        statsd.incr('http.500')
        statsd.timing(request._name,
                      int(1000 * (time.time() - request._start)))
