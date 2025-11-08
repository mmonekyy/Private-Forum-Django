from django.db import models
from forum_users.models import CustomUser
from datetime import datetime , timedelta

# Create your models here.
def works_until_default():
    date = datetime.now() + timedelta(days=30)
    return date

class Vips(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    buyed_date = models.DateTimeField(auto_now_add=True)
    works_until = models.DateTimeField(default=works_until_default())
    payment_id = models.CharField(max_length=255, null=True, blank=True)
    payer_id = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2 , default=None)
    status = models.CharField(max_length=50, default='created')
    def __str__(self):
        return f"{self.user.username} - {self.payment_id} ({self.status})"

class Button(models.Model):
    next_roll = models.DateTimeField(default=None,null=True, blank=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)

