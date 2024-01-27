from django.shortcuts import render
from app.forms import CommentForm, SubscribeForm
from app.models import Comments, Post, Tag, Profile
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.db.models import Count
from django.urls import reverse

def index(request):
    posts = Post.objects.all()
    popular_posts = posts.order_by('-view_count')[0:3]
    recent_posts = posts.order_by('-last_updated')[0:3]
    featured_post = Post.objects.filter(is_featured=True)   
    if featured_post: featured_post = featured_post[0]
    subscribe_form = SubscribeForm()
    success_message = None
    
    if request.POST:
        subscribe_form = SubscribeForm(request.POST)
        if subscribe_form.is_valid():
            subscribe_form.save()
            subscribe_form = SubscribeForm()
            success_message = 'Subscribed Successfully!'
            
    context = {
        'posts': posts, 'popular_posts': popular_posts, 'recent_posts': recent_posts, 
        'subscribe_form': subscribe_form, 'success_message': success_message, 'featured_post': featured_post
    }
    return render(request, 'app/index.html', context)

def post_page(request, slug):
    post = Post.objects.get(slug=slug)
    comments = Comments.objects.filter(post=post, parent=None)
    form = CommentForm()
    
    if request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid:
            if request.POST.get('parent'):
                parent_id = request.POST.get('parent')
                parent = Comments.objects.get(id=parent_id)
                if parent:
                    comment_reply = comment_form.save(commit=False)
                    comment_reply.parent = parent
                    comment_reply.post = post
                    comment_reply.save()
                    return HttpResponseRedirect(f'{reverse('post_page', kwargs={ 'slug': slug })}#reply-{comment_reply.id}')
            else:
                comment = comment_form.save(commit=False)
                post_id = request.POST.get('post_id')
                post = Post.objects.get(id=post_id)
                comment.post = post
                comment.save()
                return HttpResponseRedirect(f'{reverse('post_page', kwargs={ 'slug': slug })}#comment-{comment.id}')
                 
    post.view_count = 1 if post.view_count is None else post.view_count + 1
    post.save()
    
    context = { 'post': post, 'form': form, 'comments': comments }
    return render(request, 'app/post.html', context)

def tag_page(request, slug):
    tags = Tag.objects.all()
    tag = Tag.objects.get(slug=slug)
    top_posts = Post.objects.filter(tags__in=[tag.id]).order_by('-view_count')[0:2]
    recent_posts = Post.objects.filter(tags__in=[tag.id]).order_by('-last_updated')[0:2]
    
    context = { 'tags': tags, 'tag': tag, 'top_posts': top_posts, 'recent_posts': recent_posts }
    return render(request, 'app/tag.html', context)

def author_page(request, slug):
    profile = Profile.objects.get(slug=slug)
    top_authors = User.objects.annotate(number=Count('post')).order_by('number')
    top_posts = Post.objects.filter(author=profile.user).order_by('-view_count')[0:2]
    recent_posts = Post.objects.filter(author=profile.user).order_by('-last_updated')[0:2]

    context = { 'profile': profile, 'top_authors': top_authors, 'top_posts': top_posts, 'recent_posts': recent_posts }
    return render(request, 'app/author.html', context)

def search(request):
    query = ''
    if request.GET.get('q'):
        query = request.GET.get('q')
    posts = Post.objects.filter(title__icontains=query)
    
    context = { 'query': query, 'posts': posts }
    return render(request, 'app/search.html', context)
