from django.utils.text import slugify
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from .utils import generate_thumbnail_bytes, get_video_duration_file

def save(self, *args, **kwargs):
    # slug
    if not self.slug:
        base = slugify(self.title); slug = base; n = 1
        while Video.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base}-{n}"; n += 1
        self.slug = slug

    creating = self._state.adding

    # detect if file changed (only if updating)
    old_thumb_name = None
    file_changed = False
    if not creating and self.pk:
        old = Video.objects.only("video_file", "thumbnail").get(pk=self.pk)
        file_changed = old.video_file.name != self.video_file.name
        old_thumb_name = old.thumbnail.name if file_changed else None

    super().save(*args, **kwargs)  # ensure file is stored

    changed = []
    if self.video_file and (creating or file_changed or not self.duration):
        self.video_file.open("rb")
        try:
            self.duration = get_video_duration_file(self.video_file)
            changed.append("duration")
        finally:
            self.video_file.close()

    if self.video_file and (creating or file_changed) or (not self.thumbnail):
        # delete old thumb if replacing
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