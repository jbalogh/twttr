from django.db.backends.mysql.base import *

from statsd import statsd


class CursorWrapper(CursorWrapper):

    def execute(self, query, args=None):
        statsd.incr('db')
        with statsd.timer('db'):
            return super(CursorWrapper, self).execute(query, args)

class DatabaseWrapper(DatabaseWrapper):

    def _cursor(self):
        super(DatabaseWrapper, self)._cursor()
        return CursorWrapper(self.connection.cursor())
