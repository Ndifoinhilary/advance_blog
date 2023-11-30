from django.shortcuts import render, get_object_or_404
from blog import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from blog.forms import EmailPostForm

# Create your views here.


def post_list(request):
    posts = models.Post.published.all()
    paginator = Paginator(posts, 3)
    page_number = request.GET.get("page", 1)
    try:
        post_page = paginator.page(page_number)
    except PageNotAnInteger:
        post_page = paginator.page(1)
    except EmptyPage:
        post_page = paginator.page(paginator.num_pages)
    context = {"posts": posts, "post_page": post_page}
    return render(request, "blog/post/list.html", context)


def post_dettail(request, year, month, day, post):
    post = get_object_or_404(
        models.Post,
        status=models.Post.Status.PUBLISHED,
        publish__year=year,
        publish__month=month,
        publish__day=day,
        slug=post,
    )
    context = {"post": post}
    return render(request, "blog/post/detail.html", context)


def post_share(request, post_id):
    post = get_object_or_404(
        models.Post, id=post_id, status=models.Post.Status.PUBLISHED
    )
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
    else:
        form = EmailPostForm()
        return render(request, "blog/post/share.html", {"post": post, "form": form})
