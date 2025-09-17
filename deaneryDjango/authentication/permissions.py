"""
Система прав доступа для электронного деканата
"""

from functools import wraps
from django.shortcuts import redirect
from core.models import User


def get_user_role(user_id):
    """Определяет роль пользователя по его ID"""
    try:
        user = User.objects.get(user_id=user_id)
        username = user.username.lower()
        
        if username == 'admin':
            return 'admin'
        elif username == 'teacher' or 'teacher' in username:
            return 'teacher'
        else:
            return 'student'
    except User.DoesNotExist:
        return None


def requires_role(allowed_roles):
    """
    Декоратор для проверки роли пользователя.
    allowed_roles может быть строкой или списком строк.
    """
    if isinstance(allowed_roles, str):
        allowed_roles = [allowed_roles]
    
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Проверяем, залогинен ли пользователь
            if 'user_id' not in request.session:
                return redirect('authentication:login')
            
            # Получаем роль пользователя
            user_role = get_user_role(request.session['user_id'])
            
            if user_role is None:
                return redirect('authentication:login')
            
            # Проверяем, есть ли у пользователя нужная роль
            if user_role not in allowed_roles:
                return redirect('authentication:access_denied')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def admin_required(view_func):
    """Декоратор для доступа только администраторам"""
    return requires_role('admin')(view_func)


def teacher_or_admin_required(view_func):
    """Декоратор для доступа преподавателям и администраторам"""
    return requires_role(['teacher', 'admin'])(view_func)


def student_or_admin_required(view_func):
    """Декоратор для доступа студентам и администраторам"""
    return requires_role(['student', 'admin'])(view_func)