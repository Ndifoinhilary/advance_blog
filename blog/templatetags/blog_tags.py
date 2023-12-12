from django import template
from django.db.models import Count
from blog import models

register = template.Library()


@register.simple_tag
def total_posts():
    return models.Post.published.count()


@register.inclusion_tag("blog/post/latest_posts.html")
def show_latest_post(count=5):
    latest_posts = models.Post.published.order_by("-publish")[:count]
    return {"latest_posts": latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    return models.Post.published.annotate(total_commets=Count("comments")).order_by(
        "-total_commets"
    )[:count]
