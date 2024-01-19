from django.shortcuts import render
from app.models import Post

def index(request):
    context = { 'posts': Post.objects.all() }
    return render(request, 'app/index.html', context)

def post_page(request, slug):
    context = { 'post': Post.objects.get(slug=slug) }
    return render(request, 'app/post.html', context)
