from django.shortcuts import render,get_object_or_404
from blog import models
# Create your views here.



def post_list(request):
    post = models.Post.published.all()
    context = {
        'post':post
    }
    return render(request, 'blog/post/list.html', context)

def post_dettail(request, id):
    post = get_object_or_404(models.Post, id=id , status = models.Post.Status.PUBLISHED)
    context = {
        'post':post
    }
    return render(request, 'blog/post/detail.html', context)