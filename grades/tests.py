from django.test import TestCase
from users.models import CustomUser
from grades.models import Grade, Class  # Assuming you renamed Subject to Unit

class GradeModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='u', password='p')
        self.unit = Class.objects.create(name='Mathematical Foundations', description='Math core')

    def test_grade_str(self):
        grade = Grade.objects.create(
            user=self.user,
            unit=self.unit,
            grade='A',
            semester='1',
            year=2024
        )
        self.assertIn('Mathematical Foundations', str(grade))
