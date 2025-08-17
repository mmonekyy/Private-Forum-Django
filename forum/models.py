from django.db import models

# Create your models here.
class category_choices(models.Model):
    category = models.CharField(max_length=100, default='No celected')

    def __str__(self):
        return self.category