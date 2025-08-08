from django.db import models
from forum_users.models import CustomUser
from taggit.managers import TaggableManager
# Create your models here.
# Dospiać zeby w kay wards nie przekrawczało jakiej stam liczy znaków zeby jeden kayward tego nie robił 
# To do views
class Post(models.Model):
    Title = models.CharField(max_length=100)
    tags = TaggableManager()
    Text = models.TextField(max_length=5000)
    Add_date = models.DateTimeField(auto_now_add=True)
    class Status(models.IntegerChoices):
        PENDING_REVIEW = 1, 'pending_review'
        TO_EDIT = 2, 'to edit'
        APPROVED = 3,'approved'
    Post_status = models.CharField(choices=Status,default=1)
    Author = models.ForeignKey(CustomUser,on_delete=models.CASCADE)