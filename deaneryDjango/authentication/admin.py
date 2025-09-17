from django.contrib import admin
from .models import UserSession


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'ip_address', 'start_time', 'last_activity', 'is_active')
    list_filter = ('is_active', 'start_time')
    search_fields = ('user__username', 'ip_address')
    date_hierarchy = 'start_time'
