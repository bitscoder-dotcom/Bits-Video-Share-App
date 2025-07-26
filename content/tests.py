from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Video

User = get_user_model()

class VideoModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            user_type=2
        )
        
        Video.objects.create(
            title='Test Video',
            description='Test Description',
            uploader=test_user,
            video_file='test.mp4'
        )
    
    def test_video_creation(self):
        video = Video.objects.get(id=1)
        self.assertEqual(video.title, 'Test Video')
        self.assertEqual(video.uploader.username, 'testuser')
