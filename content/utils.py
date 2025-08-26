import subprocess, tempfile
from PIL import Image
from io import BytesIO

FFMPEG = "ffmpeg"   # or os.getenv("FFMPEG_PATH", "ffmpeg")
FFPROBE = "ffprobe" # or os.getenv("FFPROBE_PATH", "ffprobe")

def get_video_duration_file(file_obj) -> int:
    file_obj.seek(0)
    with tempfile.NamedTemporaryFile(suffix=".mp4") as tmp:
        tmp.write(file_obj.read()); tmp.flush()
        out = subprocess.check_output(
            [FFPROBE, "-v", "error", "-show_entries", "format=duration",
             "-of", "default=nokey=1:noprint_wrappers=1", tmp.name]
        ).decode().strip()
        return int(float(out or 0))

def generate_thumbnail_bytes(file_obj, time_in_seconds=10) -> bytes:
    file_obj.seek(0)
    with tempfile.NamedTemporaryFile(suffix=".mp4") as tmp_in, \
         tempfile.NamedTemporaryFile(suffix=".jpg") as tmp_out:
        tmp_in.write(file_obj.read()); tmp_in.flush()
        subprocess.check_call([
            FFMPEG, "-ss", str(time_in_seconds), "-i", tmp_in.name,
            "-frames:v", "1", "-q:v", "2", tmp_out.name, "-y"
        ])
        # optional resize to 320x180
        img = Image.open(tmp_out.name)
        img.thumbnail((320, 180))
        buf = BytesIO()
        img.save(buf, format="JPEG")
        return buf.getvalue()