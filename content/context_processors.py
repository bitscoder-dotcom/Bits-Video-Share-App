from .models import VideoCategory

def video_categories(request):
    return {
        'video_categories': VideoCategory.objects.all()
    }