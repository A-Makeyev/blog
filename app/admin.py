from django.contrib import admin
from app.models import Post, Tag, Comments, Subscribe, Profile, WebsiteMeta

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Comments)
admin.site.register(Subscribe)
admin.site.register(Profile)
admin.site.register(WebsiteMeta)
