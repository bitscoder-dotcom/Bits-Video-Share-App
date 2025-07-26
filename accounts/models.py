from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'consumer'),
        (2, 'creator'),
    )
    
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=1)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    
    def __str__(self):
        return self.username

class CreatorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='creator_profile')
    is_approved = models.BooleanField(default=False)
    channel_name = models.CharField(max_length=100)
    channel_description = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Creator Profile"
