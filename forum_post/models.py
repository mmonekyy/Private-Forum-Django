from django.db import models
from forum_users.models import CustomUser
from taggit.managers import TaggableManager

class Category(models.Model):
    Name = models.CharField(max_length=100)
    Description = models.TextField(max_length=500)
    
    def __str__(self):
        return self.Name

class ForumPost(models.Model):
    Title = models.CharField(max_length=200)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    Content = models.TextField()
    Author = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    Created_at = models.DateTimeField(auto_now_add=True)
    Updated_at = models.DateTimeField(auto_now=True)
    tags = TaggableManager()    
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    Post = models.ForeignKey(ForumPost,on_delete=models.CASCADE,related_name='comments')
    Author = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    Content = models.TextField()
    Created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.Author} on {self.Post}'
    