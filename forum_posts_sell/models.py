from django.db import models
from forum_users.models import CustomUser
from forum.models import category_choices
from taggit.managers import TaggableManager
# Create your models here.
# Dospiać zeby w kay wards nie przekrawczało jakiej stam liczy znaków zeby jeden kayward tego nie robił 
# To do views
class sell_post(models.Model):
    Title = models.CharField(max_length=100)
    tags = TaggableManager()
    Text = models.TextField(max_length=5000)
    Add_date = models.DateField(auto_now_add=True)
    class Status(models.IntegerChoices):
        PENDING_REVIEW = 1, 'pending_review'
        TO_EDIT = 2, 'to edit'
        APPROVED = 3,'approved'
    Post_status = models.IntegerField(choices=Status,default=1)
    Price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    #Category = models.ForeignKey(category_choices,on_delete=models.CASCADE)
    Author = models.ForeignKey(CustomUser,on_delete=models.CASCADE)