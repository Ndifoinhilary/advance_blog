from django.shortcuts import render
from blog import models
# Create your views here.



def post_list(request):
    post = models.Post.published.all()
    context = {
        'post':post
    }
    return render(request, 'blog/post/list.html', context)