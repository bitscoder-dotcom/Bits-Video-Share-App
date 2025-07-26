import os
import subprocess
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Video

@receiver(pre_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding Video object is deleted.
    """
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)
    
    if instance.thumbnail:
        if os.path.isfile(instance.thumbnail.path):
            os.remove(instance.thumbnail.path)

@receiver(post_save, sender=Video)
def process_video_after_upload(sender, instance, created, **kwargs):
    """
    Process video after upload (generate thumbnail, get duration, etc.)
    """
    if created and instance.video_file:
        # These operations are now handled in the save method
        pass
