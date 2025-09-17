from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime, timedelta
from .models import Class, Attendance
from core.models import Group, Subject, User
from teachers.models import Teacher
from students.models import Student
from authentication.permissions import teacher_or_admin_required, student_or_admin_required, get_user_role


@teacher_or_admin_required
def schedule_list(request):
    """Общее расписание - доступ только преподавателям и администраторам"""
    classes = Class.objects.all()[:20]  # Берем первых 20 занятий
    
    context = {
        'classes': classes,
        'message': 'Расписание занятий (демонстрационная версия)'
    }
    return render(request, 'schedule/schedule_list.html', context)


@teacher_or_admin_required
def class_detail(request, class_id):
    """Детальная информация о занятии"""
    try:
        class_obj = Class.objects.get(class_id=class_id)
        attendance_records = Attendance.objects.filter(class_session_id=class_id)
        
        context = {
            'class': class_obj,
            'attendance_records': attendance_records,
            'message': 'Детали занятия (демонстрационная версия)'
        }
        return render(request, 'schedule/class_detail.html', context)
    except Class.DoesNotExist:
        from django.http import Http404
        raise Http404("Занятие не найдено")


@student_or_admin_required
def my_schedule(request):
    """Мое расписание - доступ студентам для просмотра своего расписания"""
    user_id = request.session.get('user_id')
    user_role = get_user_role(user_id)
    
    if user_role == 'admin':
        # Админ видит все расписание
        classes = Class.objects.all()[:20]
        message = 'Все расписание (режим администратора)'
    else:
        # Студент видит только свое расписание
        try:
            user = User.objects.get(user_id=user_id)
            student = Student.objects.filter(first_name__icontains=user.username).first()
            if student and student.group_id:
                classes = Class.objects.filter(group_id=student.group_id)[:20]
                message = f'Расписание группы студента {user.username}'
            else:
                classes = []
                message = 'Группа студента не найдена в базе данных'
        except (User.DoesNotExist, Student.DoesNotExist):
            classes = []
            message = 'Ошибка получения данных студента'
    
    context = {
        'classes': classes,
        'message': message
    }
    return render(request, 'schedule/my_schedule.html', context)
