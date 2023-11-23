from django.db import models
from django.utils import timezone

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length = 255)
    slug = models.SlugField(max_length=255)
    body = models.TextField()
    publish = models.DateTimeField(defualt = timezone.now())
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-publish']
        indexes = [ models.Index(fields = ['-publish']),]
    def __str__(self):
        return self.title