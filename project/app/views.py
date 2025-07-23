from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category
from .forms import PostForm, CommentForm
from django.core.paginator import Paginator
from django.db.models import Q


def home(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    posts = Post.objects.all()
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))
    if category:
        posts = posts.filter(category__id=category)
    paginator = Paginator(posts.order_by('-created_at'), 5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    categories = Category.objects.all()
    return render(request, 'blog_home.html', {'posts': posts, 'categories': categories})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.all().order_by('-created_at')
    form = CommentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        return redirect('post_detail', slug=slug)
    return render(request, 'post_detail.html', {'post': post, 'form': form, 'comments': comments})


def create_post(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('home')
    return render(request, 'post_form.html', {'form': form})


def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('post_detail', slug=post.slug)
    return render(request, 'post_form.html', {'form': form})


def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request, 'confirm_delete.html', {'post': post})