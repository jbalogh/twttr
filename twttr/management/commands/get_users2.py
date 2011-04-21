from datetime import datetime
import logging
import random
import time

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connection
import django.db.utils

import MySQLdb as mysql
import twitter

from twttr.models import User, Tweet

log = logging.getLogger('seed')


def parse_dt(time):
    return datetime.strptime(time, '%a %b %d %H:%M:%S +0000 %Y')


def fill(users, all_user_ids):
    log.info('Filling.')
    api = twitter.Api(*settings.OAUTH)
    users = dict((u.id, u) for u in users)
    lookup = api.UsersLookup(users.keys())
    for user in lookup:
        u = users[unicode(user.id)]
        u.name = user.name
        u.screen_name = user.screen_name
        u.avatar_url = user.profile_image_url
        u.save()

        if user.status:
            try:
                tweet = user.status
                created = parse_dt(tweet.created_at)
                Tweet.objects.create(id=tweet.id, user=u, created=created,
                                     source=tweet.source, text=tweet.text)
            except mysql.Warning:
                pass
        log.info('Added %r.' % u)

    for user in users.values():
        try:
            friends = map(unicode, api.GetFriendIDs(user.id)['ids'])
        except twitter.TwitterError:
            if api.GetRateLimitStatus()['remaining_hits'] == 0:
                break
            else:
                continue
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

    print 'API hits left', api.GetRateLimitStatus()['remaining_hits']


class Command(BaseCommand):
    """Fetch data for users we haven't filled out yet."""

    def handle(self, *args, **kw):
        api = twitter.Api(*settings.OAUTH)
        rate_limit = api.GetRateLimitStatus()
        if rate_limit['remaining_hits'] == 0:
            reset = datetime.fromtimestamp(rate_limit['reset_time_in_seconds'])
            wait = (reset - datetime.now()).seconds
            log.info('Rate limit hit. Sleeping for %s seconds.' % wait)
            time.sleep(wait + 10)

        cursor = connection.cursor()
        cursor.execute('SELECT id FROM users')
        result = cursor.fetchall()
        all_user_ids = set(r[0] for r in result)
        log.info('%s users so far.' % len(all_user_ids))

        ids = random.sample(all_user_ids, 200)
        users = User.objects.filter(id__in=ids, name__isnull=True)[:100]
        fill(users, all_user_ids)
