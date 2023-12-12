from django import template

from blog import models

register = template.Library()


@register.simple_tag
def total_posts():
    return models.Post.published.count()
