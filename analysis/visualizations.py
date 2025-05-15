import matplotlib.pyplot as plt
import numpy as np
from .utils import get_semester_gpa_data, get_course_category_stats, analyze_user_grades, GRADE_POINTS
from grades.models import Grade
import plotly.graph_objects as go
import plotly.express as px
import json
import plotly.utils

# Visualization functions have been removed as requested 

def create_grade_distribution_chart(grade_distribution):
    """Create a bar chart for grade distribution"""
    fig = go.Figure(data=[
        go.Bar(
            x=list(grade_distribution.keys()),
            y=list(grade_distribution.values()),
            marker_color=['#28a745', '#17a2b8', '#ffc107', '#fd7e14', '#dc3545', '#6c757d'],
            text=list(grade_distribution.values()),
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title='Grade Distribution',
        xaxis_title='Grade',
        yaxis_title='Number of Units',
        template='plotly_white',
        showlegend=False,
        height=400,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return json.dumps(fig.to_dict(), cls=plotly.utils.PlotlyJSONEncoder)

def create_gpa_trend_chart(semesters, gpa_trend):
    """Create a line chart for GPA trend"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=semesters,
        y=gpa_trend,
        mode='lines+markers',
        name='GPA',
        line=dict(color='#3498db', width=3),
        marker=dict(size=8),
        fill='tozeroy',
        fillcolor='rgba(52, 152, 219, 0.1)'
    ))
    
    fig.update_layout(
        title='GPA Trend Over Time',
        xaxis_title='Semester',
        yaxis_title='GPA',
        template='plotly_white',
        showlegend=False,
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        yaxis=dict(range=[0, 4])
    )
    
    return json.dumps(fig.to_dict(), cls=plotly.utils.PlotlyJSONEncoder)

def create_failing_units_chart(semesters, failing_units):
    """Create a bar chart for failing units per semester"""
    fig = go.Figure(data=[
        go.Bar(
            x=semesters,
            y=failing_units,
            marker_color='#dc3545',
            text=failing_units,
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title='Failing Units per Semester',
        xaxis_title='Semester',
        yaxis_title='Number of Failing Units',
        template='plotly_white',
        showlegend=False,
        height=400,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return json.dumps(fig.to_dict(), cls=plotly.utils.PlotlyJSONEncoder)

def create_radar_chart(course_stats):
    """Create a radar chart for course category performance"""
    categories = list(course_stats.keys())
    values = [stats['average_gpa'] for stats in course_stats.values()]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Your Performance',
        line_color='#3498db'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 4]
            )
        ),
        showlegend=False,
        height=400,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return json.dumps(fig.to_dict(), cls=plotly.utils.PlotlyJSONEncoder)

def create_heatmap(semester_data, course_stats):
    """Create a heatmap of grades by semester and course category"""
    # Create a matrix of grades
    semesters = sorted(set(data['semester'] for data in semester_data))
    categories = list(course_stats.keys())
    
    # Initialize the matrix with zeros
    matrix = [[0 for _ in categories] for _ in semesters]
    
    # Fill the matrix with average GPAs
    for i, semester in enumerate(semesters):
        for j, category in enumerate(categories):
            if category in course_stats:
                matrix[i][j] = course_stats[category]['average_gpa']
    
    fig = go.Figure(data=go.Heatmap(
        z=matrix,
        x=categories,
        y=semesters,
        colorscale='RdYlGn',
        zmin=0,
        zmax=4
    ))
    
    fig.update_layout(
        title='Grade Heatmap by Semester and Category',
        xaxis_title='Course Category',
        yaxis_title='Semester',
        height=400,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return json.dumps(fig.to_dict(), cls=plotly.utils.PlotlyJSONEncoder) 