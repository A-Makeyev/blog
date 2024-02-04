from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='images/', null=True, blank=True)
    slug = models.SlugField(max_length=200, unique=True)
    bio = models.CharField(max_length=200)
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.user.username)
        return super(Profile, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.user.first_name
    
class Subscribe(models.Model):
    email = models.EmailField(max_length=200)
    date = models.DateTimeField(auto_now=True)

class Tag(models.Model):
    name  = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True)
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        return super(Tag, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
class Post(models.Model):
    title = models.CharField(max_length=200)
    last_updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200, unique=True)
    view_count = models.IntegerField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='post')
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    bookmarks = models.ManyToManyField(User, related_name='bookmarks', default=None, blank=True)
    likes = models.ManyToManyField(User, related_name='likes', default=None, blank=True)
    is_featured = models.BooleanField(default=False)
    content = models.TextField()
    
    def like_count(self):
        return self.likes.count()
    
class Comments(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    website = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    parent = models.ForeignKey('self', related_name='replies', on_delete=models.DO_NOTHING, null=True, blank=True)
    content = models.TextField()
    
class WebsiteMeta(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=400)
    about = models.TextField()
    