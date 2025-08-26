#!/bin/bash
set -e

FFDIR=/home/site/ffmpeg
if [ ! -x "$FFDIR/ffprobe" ]; then
  echo "Installing ffmpeg/ffprobe..."
  mkdir -p "$FFDIR"
  cd "$FFDIR"
  curl -L -o ffmpeg.tar.xz https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz
  tar -xJf ffmpeg.tar.xz --strip-components=1
  chmod +x ffmpeg ffprobe
fi

export PATH="$FFDIR:$PATH"

echo "Running migrations and collectstatic..."
python manage.py migrate --noinput
python manage.py collectstatic --noinput

echo "Starting gunicorn..."
exec gunicorn videoshare.wsgi:application --bind=0.0.0.0:${PORT} --workers=2 --threads=4 --timeout=120