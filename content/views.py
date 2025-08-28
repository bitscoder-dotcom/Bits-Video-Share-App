import os
import subprocess
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Avg, Count
from .models import Like, Video, Comment, Rating, VideoCategory
from .forms import VideoUploadForm, CommentForm, RatingForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Video, Comment, Rating, VideoCategory, Like
from .thumbnailing import generate_thumbnail_for


def home(request):
    latest_videos = Video.objects.filter(is_published=True).order_by('-created_at')[:8]
    popular_videos = Video.objects.filter(is_published=True).annotate(
        avg_rating=Avg('ratings__rating'),
        comment_count=Count('comments')
    ).order_by('-views', '-avg_rating')[:8]
    
    short_videos = Video.objects.filter(
        is_published=True,
        video_type='short'
    ).order_by('-created_at')[:4]
    
    categories = VideoCategory.objects.all()[:6]
    
    context = {
        'latest_videos': latest_videos,
        'popular_videos': popular_videos,
        'short_videos': short_videos,
        'categories': categories,
    }
    return render(request, 'home.html', context)

def video_list(request):
    videos = Video.objects.filter(is_published=True).order_by('-created_at')
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        videos = videos.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(uploader__username__icontains=query)
        )
    
    # Filter by category
    category_slug = request.GET.get('category')
    if category_slug:
        videos = videos.filter(category__slug=category_slug)
    
    # Filter by age rating
    age_rating = request.GET.get('age_rating')
    if age_rating:
        videos = videos.filter(age_rating=age_rating)
    
    # Filter by video type
    video_type = request.GET.get('video_type')
    if video_type:
        videos = videos.filter(video_type=video_type)
    
    # Pagination
    paginator = Paginator(videos, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = VideoCategory.objects.all()
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'query': query,
    }
    return render(request, 'content/video_list.html', context)

def short_videos(request):
    shorts = Video.objects.filter(
        is_published=True,
        video_type='short'
    ).order_by('-created_at')
    
    paginator = Paginator(shorts, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'content/short_videos.html', context)

def video_detail(request, slug):
    video = get_object_or_404(Video, slug=slug, is_published=True)
    
    # Increment view count
    if not request.user == video.uploader:
        video.increment_views()
    
    # Get related videos
    related_videos = Video.objects.filter(
        is_published=True,
        category=video.category
    ).exclude(id=video.id).order_by('-created_at')[:4]
    
    # Get comments
    comments = video.comments.all().order_by('-created_at')
    
    # Get average rating
    avg_rating = video.ratings.all().aggregate(Avg('rating'))['rating__avg']
    
    # Get like count and user like status
    like_count = video.likes.count()
    user_liked = False
    if request.user.is_authenticated:
        user_liked = video.likes.filter(user=request.user).exists()
    
    # Check if user has rated
    user_rating = None
    if request.user.is_authenticated:
        try:
            user_rating = Rating.objects.get(video=video, user=request.user).rating
        except Rating.DoesNotExist:
            pass
    
    # Comment form
    comment_form = CommentForm()
    
    # Rating form
    rating_form = RatingForm()
    
    context = {
        'video': video,
        'related_videos': related_videos,
        'comments': comments,
        'avg_rating': avg_rating,
        'user_rating': user_rating,
        'comment_form': comment_form,
        'rating_form': rating_form,
        'like_count': like_count,
        'user_liked': user_liked,
    }
    return render(request, 'content/video_detail.html', context)

@login_required
def video_upload(request):
    if request.user.user_type != 2:
        messages.error(request, 'Only creators can upload videos!')
        return redirect('home')
    
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.uploader = request.user

            # Set video type based on duration (if your model populates duration)
            if video.duration and video.duration <= 60:
                video.video_type = 'short'

            # Save first so it gets a PK and the file is stored in Azure
            video.save()

            # Generate & save the thumbnail to Azure
            try:
                generate_thumbnail_for(video)
            except Exception as e:
                # Don't block the upload if ffmpeg fails — just log a warning
                import logging
                logging.getLogger(__name__).warning("Thumbnail generation failed for %s: %s", video.slug, e)

            messages.success(request, 'Video uploaded successfully!')
            return redirect('content:video_detail', slug=video.slug)
    else:
        form = VideoUploadForm()
    
    return render(request, 'content/video_upload.html', {'form': form})


@login_required
@require_POST
def add_comment(request, slug):
    video = get_object_or_404(Video, slug=slug, is_published=True)
    form = CommentForm(request.POST)
    
    if form.is_valid():
        comment = form.save(commit=False)
        comment.video = video
        comment.user = request.user
        comment.save()
        messages.success(request, 'Comment added successfully!')
    else:
        messages.error(request, 'Error adding comment.')
    
    return redirect('content:video_detail', slug=slug)

@login_required
@require_POST
def add_rating(request, slug):
    video = get_object_or_404(Video, slug=slug, is_published=True)
    form = RatingForm(request.POST)
    
    if form.is_valid():
        rating, created = Rating.objects.update_or_create(
            video=video,
            user=request.user,
            defaults={'rating': form.cleaned_data['rating']}
        )
        messages.success(request, 'Rating submitted successfully!')
    else:
        messages.error(request, 'Error submitting rating.')
    
    return redirect('content:video_detail', slug=slug)

def category_videos(request, slug):
    category = get_object_or_404(VideoCategory, slug=slug)
    videos = Video.objects.filter(
        is_published=True,
        category=category
    ).order_by('-created_at')
    
    paginator = Paginator(videos, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'content/video_list.html', context)

# Context processor for categories
def video_categories(request):
    categories = VideoCategory.objects.all()
    return {'video_categories': categories}


def home(request):
    context = {}
    return render(request, 'home.html', context)
# videoshare/views.py
from django.shortcuts import render

def home_view(request):
    return render(request, 'home.html')
@login_required
@require_POST
def toggle_like(request, slug):
    video = get_object_or_404(Video, slug=slug, is_published=True)
    
    # Check if user already liked the video
    like = Like.objects.filter(video=video, user=request.user)
    
    if like.exists():
        # Unlike
        like.delete()
        liked = False
    else:
        # Like
        Like.objects.create(video=video, user=request.user)
        liked = True
    
    return JsonResponse({
        'liked': liked,
        'like_count': video.likes.count()
    })