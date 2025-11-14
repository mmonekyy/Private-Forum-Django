from django.db import models
from forum_users.models import CustomUser
from datetime import datetime , timedelta

def works_until_default():
    date = datetime.now() + timedelta(days=30)
    return date

class Keys(models.Model):
    key = models.CharField(max_length=256)

class User_gen_kay(models.Model):
    User = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    key = models.ForeignKey(Keys, on_delete=models.SET_NULL, null=True, blank=True)
    key_created = models.DateTimeField(default=datetime.now)
    nex_key = models.DateTimeField(default=works_until_default)
