from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = (
            "DF",
            "Draft",
        )
        PUBLISHED = "PB", "Published"

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique_for_date="publish")
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=255, choices=Status.choices, default=Status.DRAFT
    )

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ["-publish"]
        indexes = [
            models.Index(fields=["-publish"]),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "blog:post_details",
            args=[self.publish.year, self.publish.month, self.publish.day, self.slug],
        )


class Comment(models.Model):
    post = models.ForeignKey("Post", related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["created"]
        indexes = [
            models.Index(fields=["created"]),
        ]

    def __str__(self):
        return f"Comment by {self.name} on {self.post}"