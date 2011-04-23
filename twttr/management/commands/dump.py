import cPickle as pickle

from django.core.management.base import BaseCommand
from django.db import connection

from twttr.models import User, Tweet


class Command(BaseCommand):

    def handle(self, *args, **kw):
        cursor = connection.cursor()
        cursor.execute('SELECT id, screen_name FROM users')
        users = dict(cursor.fetchall())

        cursor.execute('SELECT id, screen_name FROM users')
        users = dict(cursor.fetchall())
        with open('users.txt', 'w') as fd:
            pickle.dump(users, fd)

        with open('user-siege.txt', 'w') as fd:
            for name in users.itervalues():
                fd.write('http://twttr.biz/%s/\n' % name)

        cursor.execute('SELECT id, user_id FROM tweets')
        tweets = dict(cursor.fetchall())
        with open('tweets.txt', 'w') as fd:
            pickle.dump(tweets, fd)

        with open('tweet-siege.txt', 'w') as fd:
            for tweet, user_id in tweets.iteritems():
                fd.write('http://twttr.biz/%s/%s' % (users[user_id], tweet))
