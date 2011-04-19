from datetime import datetime
import logging
import time

from django.core.management.base import BaseCommand
from django.db import connection
import django.db.utils

import MySQLdb as mysql
import twitter

from twttr.models import User, Tweet

log = logging.getLogger('seed')


def parse_dt(time):
    return datetime.strptime(time, '%a %b %d %H:%M:%S +0000 %Y')


class Command(BaseCommand):
    """Fetch data for users we haven't filled out yet."""

    def handle(self, *args, **kw):
        api = twitter.Api()
        rate_limit = api.GetRateLimitStatus()
        if rate_limit['remaining_hits'] == 0:
            reset = datetime.fromtimestamp(rate_limit['reset_time_in_seconds'])
            wait = (reset - datetime.now()).seconds
            log.info('Rate limit hit. Sleeping for %s seconds.' % wait)
            time.sleep(wait + 10)

        all_user_ids = set(User.objects.values_list('id', flat=True))
        log.info('%s users so far.' % len(all_user_ids))

        for user in User.objects.filter(name__isnull=True).order_by('?')[:150]:

            try:
                timeline = api.GetUserTimeline(id=user.id, count=200)
                timeline[0].user
            except (twitter.TwitterError, IndexError):
                rate_limit = api.GetRateLimitStatus()
                if rate_limit['remaining_hits'] == 0:
                    break
                user.name = 'unknown'
                user.save()
                continue

            u = timeline[0].user
            user.name = u.name
            user.screen_name = u.screen_name
            user.avatar_url = u.profile_image_url
            user.save()
            log.info('Added %r.' % user)

            for tweet in timeline:
                created = parse_dt(tweet.created_at)
                try:
                    Tweet.objects.create(id=tweet.id, user=user, created=created,
                                         source=tweet.source, text=tweet.text)
                except mysql.Warning:
                    pass
            log.info('Added %s tweets for %r.' % (user.tweets.count(), user))

            friends = map(unicode, api.GetFriendIDs(user.id)['ids'])
            for user_id in set(friends) - all_user_ids:
                try:
                    User.objects.create(id=user_id)
                except django.db.utils.IntegrityError:
                    pass
            all_user_ids.update(friends)
            if len(friends) > 1:
                cursor = connection.cursor()
                cursor.executemany("""
                    REPLACE INTO users_friends (from_user_id, to_user_id)
                      VALUES (%s,%s)""", [(user.id, x) for x in friends])
            log.info('Added %s friends for %r.' % (user.friends.count(), user))
