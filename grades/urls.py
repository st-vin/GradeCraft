
from django.urls import path
from .views import select_units, input_grade, grade_success

urlpatterns = [
    path('select/', select_units, name='select-units'),
    path('input/', input_grade, name='input-grade'),
    path('success/', grade_success, name='grade-success'),
]
