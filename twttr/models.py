from django.db import models


class User(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255, null=True)
    screen_name = models.CharField(max_length=255, null=True)
    avatar_url = models.URLField(null=True)
    friends = models.ManyToManyField('self')

    class Meta:
        db_table = 'users'

    def __unicode__(self):
        return '%s: %s' % (self.id, self.screen_name)

    @models.permalink
    def get_absolute_url(self):
        return 'twttr.user', [self.screen_name]


class Tweet(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    user = models.ForeignKey(User, related_name='tweets')
    created = models.DateTimeField(db_index=True)
    source = models.CharField(max_length=255)
    text = models.CharField(max_length=255)

    class Meta:
        db_table = 'tweets'

    @models.permalink
    def get_absolute_url(self):
        return 'twttr.tweet', [self.user.screen_name, self.id]
