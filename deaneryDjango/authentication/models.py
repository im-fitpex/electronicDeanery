from django.db import models
from core.models import User


class UserSession(models.Model):
    """Сессии пользователей"""
    session_id = models.CharField('ID сессии', max_length=255, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    ip_address = models.GenericIPAddressField('IP адрес', null=True, blank=True)
    user_agent = models.TextField('User Agent', blank=True)
    start_time = models.DateTimeField('Время начала', auto_now_add=True)
    last_activity = models.DateTimeField('Последняя активность', auto_now=True)
    expires_at = models.DateTimeField('Истекает')
    is_active = models.BooleanField('Активна', default=True)

    class Meta:
        db_table = 'user_sessions'
        verbose_name = 'Сессия пользователя'
        verbose_name_plural = 'Сессии пользователей'

    def __str__(self):
        return f"Сессия {self.user.username} ({self.session_id[:10]}...)"
