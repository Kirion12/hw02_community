from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect
from .models import Group, Post, User
from django.contrib.auth.decorators import login_required
from .forms import PostForm

def index(request):
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context) 


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).all()[:10]
    context = {
        'group': group,
        'posts': posts,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.all()
    count = author.posts.count()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'author': author,
        'posts': posts,
        'count': count,
        'page_obj': page_obj,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk = post_id)
    author = post.author
    count = author.posts.count()
    context = {
        'post': post,
        'author' : author,
        'count': count,
    }
    return render(request, 'posts/post_detail.html', context)

@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
        return redirect('posts:profile', post_id = post.id)
    else:
        form = PostForm()
    context = {
        'form': form
    }
    return render(request, 'posts/create_post.html', context)

@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = PostForm(request.POST or None, instance=post)  
    if request.user == post.author:
        return redirect('posts:index')
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id)  
    context = {
        'form': form,
        'is_edit': True,
        'post': post,
    }
    return render(request, 'posts/create_post.html', context)