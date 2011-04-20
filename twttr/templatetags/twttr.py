import re

from django import template
from django.core.urlresolvers import reverse
from django.template.defaultfilters import stringfilter, urlize

register = template.Library()
at_re = re.compile('@(\w+)')


@register.filter
@stringfilter
def twttrize(tweet):
    def url(match):
        name = match.group(1)
        url_ = reverse('twttr.user', args=(name,))
        return '<a href="%s">@%s</a>' % (url_, name)
    return urlize(at_re.sub(url, tweet))
