from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, F
from django.core.paginator import Paginator
from unicodedata import category
from .forms import PostForm
from .models import Category, Post, Tag


# Create your views here.

def index(request):
    post_list = Post.objects.all() # Find all posts,queryset
    # paging method
    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}

    return render(request, 'blog/index.html', context)


def category_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    # Get all articles in the current category
    posts = category.post_set.all()
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'category': category, 'page_obj': page_obj}
    return render(request, 'blog/list.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    # previous and next articles implemented with article ids
    prev_post = Post.objects.filter(id__lt=post_id).last()
    next_post = Post.objects.filter(id__gt=post_id).first()
    Post.objects.filter(id = post_id).update(pv = F('pv') + 1)

    context = {'post': post, 'prev_post': prev_post, 'next_post': next_post}
    return render(request, 'blog/detail.html', context)


def search(request):
    """ Related search view """
    keyword = request.GET.get('keyword', '').strip()
    post_list = Post.objects.all()
    # No search displays all articles by default
    if keyword:
        post_list = Post.objects.filter(
            Q(title__icontains=keyword) | Q(desc__icontains=keyword) | Q(content__icontains=keyword)
        )

    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj}
    return render(request, 'blog/index.html', context)


def archives(request, year, month):
    # Article archive list page
    post_list = Post.objects.filter(add_date__year=year, add_date__month=month)
    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj, 'year': year, 'month': month}
    return render(request, 'blog/archives_list.html', context)

def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user
            post.save()
            return redirect('blog:post_detail', post_id=post.pk)
    else:
        form = PostForm()

    categories = Category.objects.all()
    tags = Tag.objects.all()

    return render(request, 'users/add_post.html', {'form': form, 'categories': categories, 'tags': tags})
