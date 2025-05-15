from django import forms
from django.forms import modelformset_factory
from .models import Grade, Class

class UnitCountForm(forms.Form):
    SEMESTER_CHOICES = [
        ('Semester 1', 'Semester 1'),
        ('Semester 2', 'Semester 2'),
    ]
    
    unit_count = forms.IntegerField(
        min_value=1,
        max_value=10,
        label="Number of Units",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    semester = forms.ChoiceField(
        choices=SEMESTER_CHOICES,
        label="Semester",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    year = forms.IntegerField(
        min_value=2000,
        max_value=2050,
        initial=2025,
        label="Year",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

def get_grade_formset(extra=1, semester=None, year=None):
    class GradeForm(forms.ModelForm):
        unit_name = forms.CharField(
            max_length=100,
            label="Unit Name",
            widget=forms.TextInput(attrs={'class': 'form-control'})
        )
        description = forms.CharField(
            required=False,
            label="Description",
            widget=forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Add any additional notes or comments about this unit'
            })
        )

        class Meta:
            model = Grade
            fields = ['unit_name', 'grade', 'description']
            exclude = ['user', 'semester', 'year', 'unit']

        def save(self, commit=True):
            instance = super().save(commit=False)
            # Create or get the Class instance
            unit, created = Class.objects.get_or_create(
                name=self.cleaned_data['unit_name'],
                defaults={'description': self.cleaned_data.get('description', '')}
            )
            if not created and self.cleaned_data.get('description'):
                unit.description = self.cleaned_data['description']
                unit.save()
            instance.unit = unit
            if commit:
                instance.save()
            return instance

    return modelformset_factory(Grade, form=GradeForm, extra=extra)
