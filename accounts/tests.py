from django.test import TestCase
from .models import CustomUser

class CustomUserModelTest(TestCase):
    def test_create_user(self):
        user = CustomUser.objects.create_user(
            username='testuser',
            password='testpass123',
            user_type=1
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.user_type, 1)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
