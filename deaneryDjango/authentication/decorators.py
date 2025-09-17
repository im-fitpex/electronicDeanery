from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def custom_login_required(view_func):
    """
    Декоратор для проверки аутентификации через нашу систему сессий
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user_id = request.session.get('user_id')
        if not user_id:
            messages.warning(request, 'Для доступа к этой странице необходимо войти в систему.')
            return redirect('authentication:login')
        return view_func(request, *args, **kwargs)
    return wrapper