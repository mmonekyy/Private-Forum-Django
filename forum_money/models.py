from django.db import models
from forum_users.models import CustomUser
from datetime import datetime

# Create your models here.

class Vips(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    buyed_date = models.DateTimeField(auto_now_add=True)
    working_date = models.DateField(default=None)

class Button(models.Model):
    button_clicked = models.DateTimeField(auto_now_add=True)
    button_work = models.DateTimeField()
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)