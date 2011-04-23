import itertools

from django.conf import settings


pool = itertools.cycle(settings.DATABASES.keys())

class MasterSlaveRouter(object):
    """A router that sets up a simple master/slave configuration"""

    def db_for_read(self, model, **hints):
        return pool.next()

    def db_for_write(self, model, **hints):
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_syncdb(self, db, model):
        return True
