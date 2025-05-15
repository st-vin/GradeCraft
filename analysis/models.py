
# Create your models here.
from django.db import models
from django.conf import settings

class AnalysisResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gpa = models.DecimalField(max_digits=4, decimal_places=2)
    classification = models.CharField(max_length=50)
    num_units = models.PositiveIntegerField()
    failing_units = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - GPA: {self.gpa} - {self.classification}"
