from django.test import TestCase
from django.urls import reverse
from users.models import CustomUser

class DashboardViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='u', password='p')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, '/accounts/login/?next=/accounts/dashboard/')

    def test_dashboard_loads_for_logged_in_user(self):
        self.client.login(username='u', password='p')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome')
