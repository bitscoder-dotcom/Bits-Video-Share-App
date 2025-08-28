import os
import shutil
import subprocess
import tempfile

from django.core.files.base import ContentFile
from django.utils.text import slugify

FFMPEG_BIN = os.getenv("FFMPEG_BIN", "ffmpeg")

def _local_copy(dj_file) -> str:
    """
    Make a local /tmp copy of a Django File (works with Azure storage).
    Returns the local path.
    """
    suffix = os.path.splitext(dj_file.name)[1] or ".mp4"
    tmp_in = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp_in.close()

    # Read from storage and write to local file
    with dj_file.open("rb") as src, open(tmp_in.name, "wb") as dst:
        shutil.copyfileobj(src, dst)
    return tmp_in.name

def generate_thumbnail_for(video_obj, at_seconds: float = 1.0) -> None:
    
    # 1) Ensure local input
    in_path = _local_copy(video_obj.video_file)

    # 2) Where to put the temp jpg
    out_path = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg").name

    # 3) Run ffmpeg (one frame)
    cmd = [
        FFMPEG_BIN,
        "-y",
        "-ss", str(at_seconds),
        "-i", in_path,
        "-frames:v", "1",
        "-q:v", "2",
        out_path,
    ]
    # Let it raise if ffmpeg fails
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # 4) Save the output bytes to the ImageField (uploads to Azure)
    # Choose a stable name in your container
    slug = getattr(video_obj, "slug", slugify(getattr(video_obj, "title", "thumb")))
    uploader_id = getattr(video_obj.uploader, "id", "unknown")
    name = f"thumbnails/user_{uploader_id}/{slug}.jpg"

    with open(out_path, "rb") as f:
        data = f.read()
    video_obj.thumbnail.save(name, ContentFile(data), save=True)

    # 5) Cleanup local temp files
    try:
        os.remove(in_path)
    except FileNotFoundError:
        pass
    try:
        os.remove(out_path)
    except FileNotFoundError:
        pass
