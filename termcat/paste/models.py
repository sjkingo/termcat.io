from django.conf import settings
from django.db import models
import hashids

hasher = hashids.Hashids(salt=settings.HASHID_SALT, min_length=4)

class Paste(models.Model):
    data = models.TextField()
    remote_ip_addr = models.GenericIPAddressField()
    created_dt = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Paste'
        verbose_name_plural = verbose_name + 's'

    def __str__(self):
        return self.data

    def __repr__(self):
        return '<Paste from {} at {}>'.format(self.remote_ip_addr, self.created_dt)

    def get_absolute_url(self):
        return settings.SITE_PREFIX + '/' + self.hashid

    @property
    def hashid(self):
        return hasher.encode(self.id)
