from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=150, blank=True)
    course = models.CharField(max_length=100, blank=True)
    current_year = models.PositiveIntegerField(null=True, blank=True)
    current_Semester = models.CharField(max_length=20, blank=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username
