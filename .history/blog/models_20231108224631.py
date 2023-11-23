from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharFields(max_length = 255)
    slug = models.SlugField(max_length=255)
    body = models.TextField()
    
    def __str__(self):
        return self.title