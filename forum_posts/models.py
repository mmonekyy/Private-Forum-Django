from django.db import models
from forum_users.models import CustomUser
from taggit.managers import TaggableManager
# Create your models here.
# Dospiać zeby w kay wards nie przekrawczało jakiej stam liczy znaków zeby jeden kayward tego nie robił 
class Post(models.Model):
    Titles = models.CharField(max_length=100)
    tags = TaggableManager()
    Text = models.TextField(max_length=5000)
    Add_date = models.DateTimeField(auto_now_add=True)
    Author = models.ForeignKey(CustomUser,on_delete=models.CASCADE)