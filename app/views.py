from django.shortcuts import redirect, render, get_object_or_404
from app.forms import CommentForm, NewUserForm, SubscribeForm
from app.models import Comments, Post, Tag, Profile, WebsiteMeta
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login
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
    website_info = None
    
    if WebsiteMeta.objects.all().exists():
        website_info = WebsiteMeta.objects.all()[0]
    
    if request.POST:
        subscribe_form = SubscribeForm(request.POST)
        if subscribe_form.is_valid():
            subscribe_form.save()
            subscribe_form = SubscribeForm()
            request.session['subscribed'] = True
            success_message = 'Subscribed Successfully!'
            
    context = {
        'website_info': website_info, 'posts': posts, 'popular_posts': popular_posts, 'recent_posts': recent_posts, 
        'featured_post': featured_post, 'subscribe_form': subscribe_form, 'success_message': success_message
    }
    return render(request, 'app/index.html', context)

def post_page(request, slug):
    post = Post.objects.get(slug=slug)
    is_bookmarked = True if post.bookmarks.filter(id=request.user.id).exists() else False
    is_liked = True if post.likes.filter(id=request.user.id).exists() else False
    likes = post.like_count()
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
    
    # sidebar
    tags = Tag.objects.all()
    related_posts = Post.objects.exclude(id=post.id).filter(author=post.author)[0:3]
    recent_posts = Post.objects.exclude(id=post.id).order_by('-last_updated')[0:3]
    top_authors = User.objects.annotate(number=Count('post')).order_by('-number')
    
    
    context = { 
        'post': post, 'form': form, 'comments': comments, 'is_bookmarked': is_bookmarked,
        'is_liked': is_liked, 'likes': likes, 'tags': tags, 'related_posts': related_posts,
        'recent_posts': recent_posts, 'top_authors': top_authors
    }
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

def about(request):
    website_info = None
    
    if WebsiteMeta.objects.all().exists():
        website_info = WebsiteMeta.objects.all()[0]
    
    context = { 'website_info': website_info }
    return render(request, 'app/about.html', context)

def signup(request):
    form = NewUserForm()
    
    if request.POST:
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    
    context = { 'form': form }
    return render(request, 'registration/signup.html', context)
    
def bookmarks(request, slug):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.bookmarks.filter(id=request.user.id).exists():
        post.bookmarks.remove(request.user)
    else:
        post.bookmarks.add(request.user)
    return HttpResponseRedirect(reverse('post_page', args=[str(slug)]))

def likes(request, slug):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post_page', args=[str(slug)]))

def bookmarked_posts(request):
    bookmarked_posts = Post.objects.filter(bookmarks=request.user)
    
    context = { 'bookmarked_posts': bookmarked_posts }
    return render(request, 'app/bookmarked_posts.html', context)

def liked_posts(request):
    liked_posts = Post.objects.filter(likes=request.user)
    
    context = { 'liked_posts': liked_posts }
    return render(request, 'app/liked_posts.html', context)
