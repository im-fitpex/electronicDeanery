from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q, Avg
from .models import Grade
from students.models import Student
from core.models import Subject, Semester, User
from authentication.permissions import teacher_or_admin_required, student_or_admin_required, get_user_role


@teacher_or_admin_required
def grade_list(request):
    """Список оценок - доступ только преподавателям и администраторам"""
    grades = Grade.objects.all()[:20]  # Берем первых 20 оценок
    
    context = {
        'grades': grades,
        'message': 'Список оценок (демонстрационная версия)'
    }
    return render(request, 'grades/grade_list.html', context)


@teacher_or_admin_required
def student_grades(request, student_id):
    """Оценки конкретного студента"""
    try:
        student = Student.objects.get(student_id=student_id)
        grades = Grade.objects.filter(student_id=student_id)[:10]
        
        context = {
            'student': student,
            'grades': grades,
            'message': 'Оценки студента (демонстрационная версия)'
        }
        return render(request, 'grades/student_grades.html', context)
    except Student.DoesNotExist:
        from django.http import Http404
        raise Http404("Студент не найден")


@student_or_admin_required  
def my_grades(request):
    """Мои оценки - доступ студентам для просмотра своих оценок"""
    user_id = request.session.get('user_id')
    user_role = get_user_role(user_id)
    
    if user_role == 'admin':
        # Админ видит все оценки
        grades = Grade.objects.all()[:20]
        message = 'Все оценки (режим администратора)'
    else:
        # Студент видит только свои оценки
        try:
            user = User.objects.get(user_id=user_id)
            student = Student.objects.filter(first_name__icontains=user.username).first()
            if student:
                grades = Grade.objects.filter(student_id=student.student_id)[:20]
                message = f'Оценки студента {user.username}'
            else:
                grades = []
                message = 'Студент не найден в базе данных'
        except (User.DoesNotExist, Student.DoesNotExist):
            grades = []
            message = 'Ошибка получения данных студента'
    
    context = {
        'grades': grades,
        'message': message
    }
    return render(request, 'grades/my_grades.html', context)
