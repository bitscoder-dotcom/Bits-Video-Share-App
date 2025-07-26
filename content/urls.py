from django.urls import path
from . import views

app_name = 'content'

urlpatterns = [
    path('', views.home, name='home'),
    path('videos/', views.video_list, name='video_list'),
    path('shorts/', views.short_videos, name='short_videos'),
    path('video/<slug:slug>/', views.video_detail, name='video_detail'),
    path('video/<slug:slug>/comment/', views.add_comment, name='add_comment'),
    path('video/<slug:slug>/rate/', views.add_rating, name='add_rating'),
    path('video/<slug:slug>/like/', views.toggle_like, name='toggle_like'),
    path('upload/', views.video_upload, name='video_upload'),
    path('category/<slug:slug>/', views.category_videos, name='category_videos'),
    
]
