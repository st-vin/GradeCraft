from django.db import models
from django.conf import settings

class FeedbackEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    input_summary = models.TextField(help_text="Context/prompt sent to Phi")
    response = models.TextField(help_text="AI-generated feedback")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for {self.user.username} on {self.created_at.strftime('%Y-%m-%d %H:%M')}"
