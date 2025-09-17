from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse
from core.models import User
import hashlib
from .permissions import get_user_role


def login_view(request):
    """Страница входа"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            try:
                # Проверяем пользователя в нашей базе данных
                user = User.objects.get(username=username)
                
                # Проверяем пароль
                if user.is_active:
                    # Простая проверка пароля (в реальном проекте используйте более безопасный метод)
                    password_hash = hashlib.sha256((password + user.salt).encode()).hexdigest()
                    
                    if password_hash == user.password_hash:
                        messages.success(request, f'Добро пожаловать, {user.username}!')
                        # Сохраняем информацию о пользователе в сессии
                        request.session['user_id'] = user.user_id
                        request.session['username'] = user.username
                        return redirect('authentication:home')
                    else:
                        messages.error(request, 'Неверный пароль.')
                else:
                    messages.error(request, 'Учетная запись заблокирована.')
                    
            except User.DoesNotExist:
                messages.error(request, 'Пользователь с таким именем не найден.')
        else:
            messages.error(request, 'Пожалуйста, заполните все поля.')
    
    return render(request, 'authentication/login.html')


def logout_view(request):
    """Выход из системы"""
    # Очищаем сессию
    request.session.flush()
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('authentication:login')


def home_view(request):
    """Главная страница"""
    user_id = request.session.get('user_id')
    current_user = None
    user_role = None
    
    if user_id:
        try:
            current_user = User.objects.get(user_id=user_id)
            user_role = get_user_role(user_id)
        except User.DoesNotExist:
            pass
    
    # Определяем доступные разделы в зависимости от роли
    available_sections = []
    if user_role == 'admin':
        available_sections = [
            {'name': 'Студенты', 'url': 'students:student_list', 'icon': 'fas fa-user-graduate'},
            {'name': 'Преподаватели', 'url': 'teachers:teacher_list', 'icon': 'fas fa-chalkboard-teacher'},
            {'name': 'Оценки', 'url': 'grades:grade_list', 'icon': 'fas fa-star'},
            {'name': 'Расписание', 'url': 'schedule:schedule_list', 'icon': 'fas fa-calendar'},
            {'name': 'Управление пользователями', 'url': 'authentication:admin_panel', 'icon': 'fas fa-users-cog'},
        ]
    elif user_role == 'teacher':
        available_sections = [
            {'name': 'Студенты', 'url': 'students:student_list', 'icon': 'fas fa-user-graduate'},
            {'name': 'Оценки', 'url': 'grades:grade_list', 'icon': 'fas fa-star'},
            {'name': 'Расписание', 'url': 'schedule:schedule_list', 'icon': 'fas fa-calendar'},
        ]
    elif user_role == 'student':
        available_sections = [
            {'name': 'Мои оценки', 'url': 'grades:my_grades', 'icon': 'fas fa-star'},
            {'name': 'Расписание', 'url': 'schedule:my_schedule', 'icon': 'fas fa-calendar'},
        ]
    
    context = {
        'message': 'Django приложение успешно запущено и подключено к базе данных PostgreSQL!',
        'current_user': current_user,
        'user_role': user_role,
        'is_logged_in': bool(current_user),
        'available_sections': available_sections,
        'apps': [
            'Основные данные (core)',
            'Студенты (students)', 
            'Преподаватели (teachers)',
            'Оценки (grades)',
            'Расписание (schedule)',
            'Аутентификация (authentication)'
        ]
    }
    return render(request, 'authentication/home.html', context)


def profile_view(request):
    """Профиль пользователя"""
    user_id = request.session.get('user_id')
    current_user = None
    user_role = None
    student_info = None
    
    if user_id:
        try:
            current_user = User.objects.get(user_id=user_id)
            user_role = get_user_role(user_id)
            
            # Если это студент, получаем дополнительную информацию
            if user_role == 'student':
                from students.models import Student
                student_info = Student.objects.filter(
                    first_name__icontains=current_user.username
                ).first()
                
        except User.DoesNotExist:
            pass
    
    context = {
        'current_user': current_user,
        'user_role': user_role,
        'student_info': student_info,
    }
    return render(request, 'authentication/profile.html', context)


def access_denied_view(request):
    """Страница отказа в доступе"""
    return render(request, 'authentication/access_denied.html')


def admin_panel_view(request):
    """Панель администратора"""
    user_id = request.session.get('user_id')
    user_role = get_user_role(user_id) if user_id else None
    
    if user_role != 'admin':
        return redirect('authentication:access_denied')
    
    # Получаем всех пользователей
    users = User.objects.all()
    
    context = {
        'users': users,
        'user_count': users.count(),
    }
    return render(request, 'authentication/admin_panel.html', context)
