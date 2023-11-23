from django.shortcuts import render,get_object_or_404
from blog import models
from django.core.paginator import Paginator

# Create your views here.



def post_list(request):
    posts = models.Post.published.all()
    context = {
        'posts':posts
    }
    return render(request, 'blog/post/list.html', context)

def post_dettail(request, year,month,day,post):
    post = get_object_or_404(models.Post, status = models.Post.Status.PUBLISHED,publish__year=year,publish__month=month,publish__day=day,slug=post)
    context = {
        'post':post
    }
    return render(request, 'blog/post/detail.html', context)