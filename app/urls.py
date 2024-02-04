from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<slug:slug>', views.post_page, name='post_page'),
    path('tag/<slug:slug>', views.tag_page, name='tag_page'),
    path('author/<slug:slug>', views.author_page, name='author_page'),
    path('search/', views.search, name='search'),
    path('about/', views.about, name='about'),
    path('accounts/signup', views.signup, name='signup'),
    path('likes/<slug:slug>', views.likes, name='likes'),
    path('bookmarks/<slug:slug>', views.bookmarks, name='bookmarks'),
    path('bookmarked_posts', views.bookmarked_posts, name='bookmarked_posts'),
    path('liked_posts', views.liked_posts, name='liked_posts'),
]
