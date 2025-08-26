# content/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from .utils import generate_thumbnail_bytes, get_video_duration_file

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
    return f"videos/user_{instance.uploader_id}/{filename}"

def thumbnail_upload_path(instance, filename):
    return f"thumbnails/user_{instance.uploader_id}/{filename}"


class Video(models.Model):
    AGE_RATING_CHOICES = [
        ('G', 'General Audiences'),
        ('PG', 'Parental Guidance Suggested'),
        ('PG-13', 'Parents Strongly Cautioned'),
        ('R', 'Restricted'),
        ('NC-17', 'Adults Only'),
    ]
    VIDEO_TYPE_CHOICES = [('short', 'Short Video'), ('long', 'Long Video')]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos')
    video_file = models.FileField(upload_to=video_upload_path)
    thumbnail = models.ImageField(upload_to=thumbnail_upload_path, blank=True, null=True)
    duration = models.PositiveIntegerField(default=0)  # seconds
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
        # slug (unique)
        if not self.slug:
            base = slugify(self.title) or "video"
            slug = base
            n = 1
            while Video.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug

        creating = self._state.adding

        # detect file change on update
        old_thumb_name = None
        file_changed = False
        if not creating and self.pk:
            old = Video.objects.only("video_file", "thumbnail").get(pk=self.pk)
            file_changed = old.video_file.name != self.video_file.name
            old_thumb_name = old.thumbnail.name if file_changed else None

        super().save(*args, **kwargs)  # ensure file stored and PK exists

        changed = []

        # duration
        if self.video_file and (creating or file_changed or not self.duration):
            self.video_file.open("rb")
            try:
                self.duration = get_video_duration_file(self.video_file)
                changed.append("duration")
            finally:
                self.video_file.close()

        # auto thumbnail
        need_thumb = (self.video_file and (creating or file_changed)) or (not self.thumbnail)
        if need_thumb:
            if old_thumb_name:
                default_storage.delete(old_thumb_name)

            self.video_file.open("rb")
            try:
                thumb_bytes = generate_thumbnail_bytes(self.video_file)
            finally:
                self.video_file.close()

            name = f"thumbnails/user_{self.uploader_id}/{self.slug}.jpg"
            stored = default_storage.save(name, ContentFile(thumb_bytes))
            self.thumbnail.name = stored
            changed.append("thumbnail")

        if changed:
            super().save(update_fields=changed)

    def increment_views(self):
        self.views = models.F('views') + 1
        super().save(update_fields=['views'])
        # refresh to get the real value if you need it afterwards
        self.refresh_from_db(fields=['views'])


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
    RATING_CHOICES = [(i, f"{i}") for i in range(1, 6)]
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('video', 'user')

    def __str__(self):
        return f"{self.rating}★ by {self.user.username} for {self.video.title}"


class Like(models.Model):
    video = models.ForeignKey(Video, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('video', 'user')

    def __str__(self):
        return f"{self.user.username} likes {self.video.title}"
