from django.db import models
from forum_users.models import CustomUser
from datetime import datetime

# Create your models here.

class Vips(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    buyed_date = models.DateTimeField(auto_now_add=True)
    working_date = models.DateField(default=None,null=True, blank=True)

class Button(models.Model):
    next_roll = models.DateTimeField(default=None,null=True, blank=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)