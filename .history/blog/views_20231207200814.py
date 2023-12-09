from django.shortcuts import render, get_object_or_404
from blog import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_POST
from django.db.models import Count
from blog.forms import EmailPostForm, CommentForm
from taggit.models import Tag

# Create your views here.


def post_list(request, tag_slug=None):
    posts = models.Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
    paginator = Paginator(posts, 3)
    page_number = request.GET.get("page", 1)
    try:
        post_page = paginator.page(page_number)
    except PageNotAnInteger:
        post_page = paginator.page(1)
    except EmptyPage:
        post_page = paginator.page(paginator.num_pages)
    context = {"posts": posts, "post_page": post_page, "tag": tag}
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
    comments = post.comments.filter(active=True)
    form = CommentForm()
    post_tags_id = post.tags.values_list("id", flat=True)
    similar_posts = models.Post.publish.filter(tags__in=post_tags_id).exclude(
        id=post.id
    )
    similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by(
        "-same_tags", "-publish"
    )[:4]
    context = {
        "post": post,
        "comments": comments,
        "fomr": form,
        "similar_posts": similar_posts,
    }
    return render(request, "blog/post/detail.html", context)


def post_share(request, post_id):
    post = get_object_or_404(
        models.Post, id=post_id, status=models.Post.Status.PUBLISHED
    )
    sent = False
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommands you read {post.title}"
            message = f"Read {post.title} at {post_url} {cd['name']} \s comments:{cd['comments']}"

            send_mail(subject, message, settings.EMAIL_HOST_USER, [cd["to"]])
            sent = True
    else:
        form = EmailPostForm()
        return render(
            request, "blog/post/share.html", {"post": post, "form": form, "sent": sent}
        )


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(
        models.Post, id=post_id, status=models.Post.Status.PUBLISHED
    )
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(
        request,
        "blog/post/comment.html",
        {"post": post, "comment": comment, "form": form},
    )
