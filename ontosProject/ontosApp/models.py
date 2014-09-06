from django.db import models

# Create your models here.

class User(models.Model):
    firstName = models.CharField(max_length=200)
    lastName = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    top10hits = []
    metadata = []
    def __unicode__(self):              # __unicode__ on Python 2
        return self.firstName



