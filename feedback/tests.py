from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from feedback.models import FeedbackEntry
from analysis.models import AnalysisResult
from unittest.mock import patch

User = get_user_model()

class FeedbackModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_feedback_entry_creation(self):
        feedback = FeedbackEntry.objects.create(
            user=self.user,
            input_summary="Test input",
            response="Test response"
        )
        self.assertEqual(feedback.user, self.user)
        self.assertEqual(feedback.input_summary, "Test input")
        self.assertEqual(feedback.response, "Test response")
        self.assertIsNotNone(feedback.created_at)
        
    def test_feedback_entry_str(self):
        feedback = FeedbackEntry.objects.create(
            user=self.user,
            input_summary="Test input",
            response="Test response"
        )
        expected_str = f"Feedback for {self.user.username} on {feedback.created_at.strftime('%Y-%m-%d %H:%M')}"
        self.assertEqual(str(feedback), expected_str)

class FeedbackViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        self.feedback_url = reverse('feedback-view')
        
    def test_feedback_view_no_analysis(self):
        response = self.client.get(self.feedback_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feedback/no_analysis.html')
        
    def test_feedback_view_with_analysis(self):
        # Create analysis result
        analysis = AnalysisResult.objects.create(
            user=self.user,
            gpa=3.5,
            failing_units=0,
            num_units=12,
            classification='Good Standing'
        )
        
        response = self.client.get(self.feedback_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feedback/view.html')
        self.assertIn('analysis', response.context)
        self.assertEqual(response.context['analysis'], analysis)
        
    @patch('feedback.services.phi.get_feedback_response')
    def test_feedback_generation(self, mock_get_feedback):
        # Create analysis result
        AnalysisResult.objects.create(
            user=self.user,
            gpa=3.5,
            failing_units=0,
            num_units=12,
            classification='Good Standing'
        )
        
        # Mock the AI response
        mock_get_feedback.return_value = "Test feedback response"
        
        response = self.client.post(self.feedback_url)
        self.assertEqual(response.status_code, 302)  # Redirect after successful POST
        
        # Verify feedback was created
        feedback = FeedbackEntry.objects.filter(user=self.user).first()
        self.assertIsNotNone(feedback)
        self.assertEqual(feedback.response, "Test feedback response")
        
    @patch('feedback.services.phi.get_feedback_response')
    def test_feedback_generation_error(self, mock_get_feedback):
        # Create analysis result
        AnalysisResult.objects.create(
            user=self.user,
            gpa=3.5,
            failing_units=0,
            num_units=12,
            classification='Good Standing'
        )
        
        # Mock the AI response to raise an exception
        mock_get_feedback.side_effect = Exception("Test error")
        
        response = self.client.post(self.feedback_url)
        self.assertEqual(response.status_code, 302)  # Redirect after error
        
        # Verify no feedback was created
        feedback = FeedbackEntry.objects.filter(user=self.user).first()
        self.assertIsNone(feedback)
        
    def test_feedback_view_requires_login(self):
        self.client.logout()
        response = self.client.get(self.feedback_url)
        self.assertEqual(response.status_code, 302)  # Redirect to login
