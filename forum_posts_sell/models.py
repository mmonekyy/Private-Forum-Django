from django.db import models
from forum_users.models import CustomUser
from forum.models import category_choices
from taggit.managers import TaggableManager
from django.utils import timezone
# Create your models here.
# Dospiać zeby w kay wards nie przekrawczało jakiej stam liczy znaków zeby jeden kayward tego nie robił 
# To do views

def get_post_life():
    return (timezone.now() + timezone.timedelta(days=14)).date()

class sell_post(models.Model):
    Title = models.CharField(max_length=100)
    tags = TaggableManager()
    Text = models.TextField(max_length=5000)
    Add_date = models.DateTimeField(auto_now_add=True)
    class Status(models.IntegerChoices):
        PENDING_REVIEW = 1, 'pending_review'
        TO_EDIT = 2, 'to edit'
        APPROVED = 3,'approved'
    Post_status = models.IntegerField(choices=Status,default=1)
    Price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    Post_life = models.DateField(default=get_post_life)
    #Category = models.ForeignKey(category_choices,on_delete=models.CASCADE)
    Author = models.ForeignKey(CustomUser,on_delete=models.CASCADE)

class buyed_item(models.Model):
    foring_key_sell_post = models.ForeignKey(sell_post,on_delete=models.CASCADE)
    Text = models.TextField(max_length=5000, default="")

class user_bought_items(models.Model):
    foring_key_buy_item = models.ForeignKey(buyed_item,on_delete=models.CASCADE)
    User = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    Add_date = models.DateTimeField(auto_now_add=True)
    
class opinion(models.Model):
    foring_key_buy_item = models.ForeignKey(sell_post,on_delete=models.CASCADE)
    Author = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    Add_date = models.DateTimeField(auto_now_add=True)
    class Rate(models.IntegerChoices):
        ONE = 1, '1'
        TWO = 2, '2'
        THREE = 3,'3'
        FOUR = 4,'4'
        FIVE = 5,'5'
    Rate = models.IntegerField(choices=Rate,default=5)
