from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
import os
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from videoshare import settings
from videoshare.settings import MEDIA_ROOT
from .utils import generate_thumbnail, get_video_duration

User = get_user_model()

class VideoCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Video Categories"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

def video_upload_path(instance, filename):
    return f'videos/user_{instance.uploader.id}/{filename}'

def thumbnail_upload_path(instance, filename):
    return f'thumbnails/user_{instance.uploader.id}/{filename}'

class Video(models.Model):
    AGE_RATING_CHOICES = [
        ('G', 'General Audiences'),
        ('PG', 'Parental Guidance Suggested'),
        ('PG-13', 'Parents Strongly Cautioned'),
        ('R', 'Restricted'),
        ('NC-17', 'Adults Only'),
    ]
    
    VIDEO_TYPE_CHOICES = [
        ('short', 'Short Video'),
        ('long', 'Long Video'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos')
    video_file = models.FileField(upload_to=video_upload_path)
    thumbnail = models.ImageField(upload_to=thumbnail_upload_path, blank=True)
    duration = models.PositiveIntegerField(default=0)  # in seconds
    views = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(VideoCategory, on_delete=models.SET_NULL, null=True, blank=True)
    age_rating = models.CharField(max_length=5, choices=AGE_RATING_CHOICES, default='G')
    video_type = models.CharField(max_length=10, choices=VIDEO_TYPE_CHOICES, default='long')
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
     if not self.slug:
        base_slug = slugify(self.title)
        slug = base_slug
        counter = 1
        while Video.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        self.slug = slug

     if not self.thumbnail and self.video_file:
        # Generate thumbnail if not provided
        thumbnail_path = generate_thumbnail(self.video_file.path)
        if thumbnail_path:
            self.thumbnail.save(
                os.path.basename(thumbnail_path),
                open(thumbnail_path, 'rb'),
                save=False
            )

     if not self.duration and self.video_file:
        self.duration = get_video_duration(self.video_file.path)

     super().save(*args, **kwargs)
    
    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])

class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.video.title}"

class Rating(models.Model):
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]
    
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('video', 'user')
    
    def __str__(self):
        return f"{self.rating} stars by {self.user.username} for {self.video.title}"
# models.py
class Like(models.Model):
    video = models.ForeignKey(Video, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('video', 'user')  # Prevent multiple likes from same user
    
    def __str__(self):
        return f"{self.user.username} likes {self.video.title}"