from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Video
from django.core.files.storage import default_storage


@receiver(post_save, sender=Video)
def process_video_after_upload(sender, instance, created, **kwargs):
    """
    Process video after upload (generate thumbnail, get duration, etc.)
    """
    if created and instance.video_file:
        # These operations are now handled in the save method
        pass

@receiver(pre_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.video_file and instance.video_file.name:
        default_storage.delete(instance.video_file.name)
    if instance.thumbnail and instance.thumbnail.name:
        default_storage.delete(instance.thumbnail.name)