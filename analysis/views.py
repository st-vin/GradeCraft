from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .utils import analyze_user_grades, get_course_category_stats, get_class_averages, get_semester_gpa_data
from .models import AnalysisResult
from grades.models import Grade
from .visualizations import (
    create_grade_distribution_chart,
    create_gpa_trend_chart,
    create_failing_units_chart,
    create_radar_chart,
    create_heatmap
)
import json

@login_required
def report_view(request):
    # Check for an existing analysis result for this user
    existing = AnalysisResult.objects.filter(user=request.user).order_by('-timestamp').first()
    
    # Always recalculate for latest data
    result_data = analyze_user_grades(request.user)
    
    if result_data:
        # Create a new AnalysisResult instance
        result = AnalysisResult.objects.create(
            user=request.user,
            gpa=result_data['gpa'],
            classification=result_data['classification'],
            num_units=result_data['num_units'],
            failing_units=result_data['failing_units'],
        )
        
        # Get additional data for analysis
        course_stats = get_course_category_stats(request.user)
        class_averages = get_class_averages(request.user)
        semester_data = get_semester_gpa_data(request.user)
        
        # Calculate grade distribution
        grades = Grade.objects.filter(user=request.user)
        grade_distribution = {
            'A': grades.filter(grade='A').count(),
            'B': grades.filter(grade='B').count(),
            'C': grades.filter(grade='C').count(),
            'D': grades.filter(grade='D').count(),
            'E': grades.filter(grade='E').count(),
            'I': grades.filter(grade='I').count(),
        }
        
        # Format semester data for charts
        semesters = [data['semester'] for data in semester_data]
        gpa_trend = [data['gpa'] for data in semester_data]
        
        # Calculate failing units per semester
        failing_units_trend = []
        for data in semester_data:
            # Split semester string into semester and year
            semester_parts = data['semester'].split()
            if len(semester_parts) >= 2:
                semester = semester_parts[0]
                year = semester_parts[1]
                failing_count = Grade.objects.filter(
                    user=request.user,
                    semester=semester,
                    year=year,
                    grade='E'
                ).count()
                failing_units_trend.append(failing_count)
            else:
                # Handle case where semester format is different
                failing_count = Grade.objects.filter(
                    user=request.user,
                    semester=data['semester'],
                    grade='E'
                ).count()
                failing_units_trend.append(failing_count)
        
        # Create visualizations
        grade_dist_chart = create_grade_distribution_chart(grade_distribution)
        gpa_trend_chart = create_gpa_trend_chart(semesters, gpa_trend)
        failing_units_chart = create_failing_units_chart(semesters, failing_units_trend)
        radar_chart = create_radar_chart(course_stats)
        heatmap_chart = create_heatmap(semester_data, course_stats)
        
        # Add the data to the context
        context = {
            'result': result,
            'previous': existing if existing and existing != result else None,
            'course_stats': json.dumps(course_stats) if course_stats else None,
            'class_averages': json.dumps(class_averages) if class_averages else None,
            'semester_data': json.dumps(semester_data) if semester_data else None,
            'grade_dist_chart': grade_dist_chart,
            'gpa_trend_chart': gpa_trend_chart,
            'failing_units_chart': failing_units_chart,
            'radar_chart': radar_chart,
            'heatmap_chart': heatmap_chart,
        }
    else:
        context = {
            'result': None,
            'previous': existing,
        }
        
    return render(request, 'analysis/report.html', context)

@login_required
def get_historical_data(request):
    """API endpoint to fetch historical GPA data"""
    historical_data = [
        {'semester': 'Sem 1', 'gpa': 3.2},
        {'semester': 'Sem 2', 'gpa': 3.5},
        {'semester': 'Sem 3', 'gpa': 3.8},
        {'semester': 'Sem 4', 'gpa': 3.6},
        {'semester': 'Current', 'gpa': 3.7},
    ]
    
    return JsonResponse({'data': historical_data})