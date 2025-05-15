from grades.models import Grade

GRADE_POINTS = {
    'A': 4.0,
    'B': 3.0,
    'C': 2.0,
    'D': 1.0,
    'E': 0.0,
    'I': 0.0,  # You could also choose to ignore this in GPA
}

CLASSIFICATION_THRESHOLDS = {
    3.7: "First Class Honours",
    3.0: "Second Class Honours (Upper)",
    2.0: "Second Class Honours (Lower)",
    1.0: "Pass",
    0.0: "Fail",
}

def classify_gpa(gpa):
    for threshold, label in CLASSIFICATION_THRESHOLDS.items():
        if gpa >= threshold:
            return label
    return "Unknown"

def analyze_user_grades(user):
    grades = Grade.objects.filter(user=user)
    if not grades.exists():
        return None

    total_points = 0
    count = 0
    failing = 0

    for grade in grades:
        letter = grade.grade
        if letter == 'I':
            continue  # skip incomplete
        points = GRADE_POINTS.get(letter, 0)
        total_points += points
        count += 1
        if letter == 'E':
            failing += 1

    gpa = round(total_points / count, 2) if count > 0 else 0.0
    classification = classify_gpa(gpa)

    return {
        'gpa': gpa,
        'classification': classification,
        'num_units': count,
        'failing_units': failing
    }

def get_course_category_stats(user):
    """
    Analyzes the grades for all courses of a specific user and returns statistics.

    Args:
        user: The user object to analyze grades for.

    Returns:
        A dictionary containing course statistics.
    """
    from grades.models import Class
    
    course_stats = {}
    courses = Class.objects.filter(grades__user=user).distinct()
    
    for course in courses:
        grades = Grade.objects.filter(unit=course, user=user)
        if not grades.exists():
            course_stats[course.name] = {
                'num_students': 0,
                'average_gpa': 0.0,
                'failing_students': 0
            }
            continue

        total_points = 0
        count = 0
        failing = 0

        for grade in grades:
            letter = grade.grade
            points = GRADE_POINTS.get(letter, 0)
            total_points += points
            count += 1
            if letter == 'E':
                failing += 1

        average_gpa = round(total_points / count, 2) if count > 0 else 0.0

        course_stats[course.name] = {
            'num_students': count,
            'average_gpa': average_gpa,
            'failing_students': failing
        }

    return course_stats

def get_class_averages(user=None):
    """
    Calculates the average GPA for all classes. Optionally filters by user.

    Args:
        user: The user object to filter grades by (optional).

    Returns:
        A dictionary where keys are class names and values are their average GPAs.
    """
    from grades.models import Class, Grade

    class_averages = {}
    classes = Class.objects.all()

    for cls in classes:
        grades = Grade.objects.filter(unit=cls)
        if user:
            grades = grades.filter(user=user)

        if not grades.exists():
            class_averages[cls.name] = 0.0
            continue

        total_points = 0
        count = 0

        for grade in grades:
            letter = grade.grade
            points = GRADE_POINTS.get(letter, 0)
            total_points += points
            count += 1

        average_gpa = round(total_points / count, 2) if count > 0 else 0.0
        class_averages[cls.name] = average_gpa

    return class_averages

def get_semester_gpa_data(user):
    """
    Calculates GPA for each semester the user has taken courses.

    Args:
        user: The user object to analyze grades for.

    Returns:
        A dictionary containing semester-wise GPA data.
    """
    from django.db.models import Avg
    from grades.models import Grade

    # Get all unique semester-year combinations for the user
    semester_data = Grade.objects.filter(user=user).values('semester', 'year').distinct().order_by('year', 'semester')
    
    semester_gpa = []
    for data in semester_data:
        # Get all grades for this semester
        grades = Grade.objects.filter(
            user=user,
            semester=data['semester'],
            year=data['year']
        )
        
        total_points = 0
        count = 0
        
        for grade in grades:
            if grade.grade == 'I':  # Skip incomplete grades
                continue
            points = GRADE_POINTS.get(grade.grade, 0)
            total_points += points
            count += 1
        
        if count > 0:
            gpa = round(total_points / count, 2)
            semester_gpa.append({
                'semester': f"{data['semester']} {data['year']}",
                'gpa': gpa
            })
    
    return semester_gpa
