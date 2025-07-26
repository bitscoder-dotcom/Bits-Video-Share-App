import os
import cv2
import numpy as np
from PIL import Image
import subprocess
import tempfile

def generate_thumbnail(video_path, time_in_seconds=10):
    """
    Generate a thumbnail from a video at the specified time.
    Returns the path to the generated thumbnail.
    """
    try:
        # Create a temporary file for the thumbnail
        temp_dir = tempfile.gettempdir()
        thumbnail_path = os.path.join(temp_dir, f"thumbnail_{os.path.basename(video_path)}.jpg")
        
        # Use ffmpeg to extract a frame at the specified time
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-ss', str(time_in_seconds),
            '-vframes', '1',
            '-q:v', '2',
            thumbnail_path,
            '-y'
        ]
        
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Resize the thumbnail to standard size
        img = Image.open(thumbnail_path)
        img.thumbnail((320, 180))
        img.save(thumbnail_path)
        
        return thumbnail_path
    except Exception as e:
        print(f"Error generating thumbnail: {e}")
        return None

def get_video_duration(video_path):
    """
    Get the duration of a video in seconds.
    """
    try:
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            video_path
        ]
        
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        duration = float(result.stdout)
        return int(duration)
    except Exception as e:
        print(f"Error getting video duration: {e}")
        return 0
