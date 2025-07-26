from django.contrib import admin
from .models import Video, Comment, Rating, VideoCategory

admin.site.register(Video)
admin.site.register(Comment)
admin.site.register(Rating)
admin.site.register(VideoCategory)
