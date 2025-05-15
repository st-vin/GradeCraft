from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from users.models import CustomUser

class CustomUserModelTest(TestCase):
    def test_create_user_with_custom_fields(self):
        user = CustomUser.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com',
            full_name='Test User',
            course='CS',
            current_year=2,
            current_Semester='Semester 1'
        )
        self.assertEqual(user.course, 'CS')
