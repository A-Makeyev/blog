from django.shortcuts import render
from app.forms import CommentForm
from app.models import Comments, Post
from django.http import HttpResponseRedirect
from django.urls import reverse

def index(request):
    context = { 'posts': Post.objects.all() }
    return render(request, 'app/index.html', context)

def post_page(request, slug):
    post = Post.objects.get(slug=slug)
    comments = Comments.objects.filter(post=post)
    form = CommentForm()
    
    if request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid:
            comment = comment_form.save(commit=False)
            post_id = request.POST.get('post_id')
            post = Post.objects.get(id=post_id)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse('post_page', kwargs={ 'slug': slug }))
    
    if post.view_count is None:
        post.view_count = 1
    else:
        post.view_count = post.view_count + 1 
    post.save()
    
    context = { 'post': post, 'form': form, 'comments': comments }
    return render(request, 'app/post.html', context)
