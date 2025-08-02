from django.db import models

class Keys(models.Model):
    key = models.CharField(max_length=255)
