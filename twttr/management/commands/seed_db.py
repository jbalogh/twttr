from datetime import datetime
import logging

from django.core.management.base import BaseCommand

import twitter

from twttr.models import User, Tweet

log = logging.getLogger('seed')


def parse_dt(time):
    return datetime.strptime(time, '%a %b %d %H:%M:%S +0000 %Y')


class Command(BaseCommand):
    """Seed the database with jeffbalogh's friends."""

    def handle(self, *args, **kw):
        api = twitter.Api()
        me = api.GetUser('jeffbalogh')
        user = User.objects.create(id=me.id, name=me.name,
                                   screen_name=me.screen_name,
                                   avatar_url=me.profile_image_url)
        log.info('Added %r.' % user)
        for tweet in api.GetUserTimeline(id=user.id, count=100):
            created = parse_dt(tweet.created_at)
            Tweet.objects.create(id=tweet.id, user=user, source=tweet.source,
                                 text=tweet.text, created=created)
        log.info('Added %s tweets for %r.' % (user.tweets.count(), user))
        for user_id in api.GetFriendIDs('jeffbalogh')['ids']:
            user.friends.add(User.objects.create(id=user_id))
        user.save()
        log.info('Added %s friends for %r.' % (user.friends.count(), user))
