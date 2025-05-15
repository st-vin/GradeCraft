from django.db import models
from django.conf import settings

# Optional: Use a CHOICES tuple for letter grades with explanations
GRADE_CHOICES = [
    ('A', 'A (70–100%) – First Class Honours'),
    ('B', 'B (60–69%) – Second Class Honours Upper'),
    ('C', 'C (50–59%) – Second Class Honours Lower'),
    ('D', 'D (40–49%) – Pass'),
    ('E', 'E (0–39%) – Fail'),
    ('I', 'I – Incomplete / Missing Marks / Deferred due to Illness'),
]

class Class(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Grade(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    grade = models.CharField(max_length=1, choices=GRADE_CHOICES)
    semester = models.CharField(max_length=20)
    year = models.PositiveIntegerField()
    date_recorded = models.DateTimeField(auto_now_add=True)
    unit = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='grades')

    def __str__(self):
        return f"{self.user.username} - ({self.grade})"
