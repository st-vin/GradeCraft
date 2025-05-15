from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UnitCountForm, get_grade_formset
from .models import Grade

@login_required
def select_units(request):
    if request.method == 'POST':
        form = UnitCountForm(request.POST)
        if form.is_valid():
            unit_count = form.cleaned_data['unit_count']
            semester = form.cleaned_data['semester']
            year = form.cleaned_data['year']
            
            # Store all these values in session
            request.session['unit_count'] = unit_count
            request.session['semester'] = semester
            request.session['year'] = year
            
            return redirect('input-grade')
    else:
        form = UnitCountForm()
    return render(request, 'grades/select_units.html', {'form': form})

@login_required
def input_grade(request):
    unit_count = request.session.get('unit_count', 1)
    semester = request.session.get('semester')
    year = request.session.get('year')
    
    if not semester or not year:
        return redirect('select-units')
    
    GradeFormSet = get_grade_formset(extra=unit_count, semester=semester, year=year)

    if request.method == 'POST':
        formset = GradeFormSet(request.POST)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for grade in instances:
                grade.user = request.user
                grade.semester = semester
                grade.year = year
                grade.save()
            return redirect('grade-success')
    else:
        formset = GradeFormSet(queryset=Grade.objects.none())

    return render(request, 'grades/input_grade.html', {
        'formset': formset,
        'semester': semester,
        'year': year
    })

from django.http import HttpResponse

@login_required
def grade_success(request):
    return HttpResponse("✅ Grades submitted successfully!")
