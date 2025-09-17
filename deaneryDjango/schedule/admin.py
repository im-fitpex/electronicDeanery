from django.contrib import admin
from .models import Class, Attendance


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('subject', 'teacher', 'group', 'class_date', 'start_time', 'end_time', 'class_type')
    list_filter = ('class_type', 'semester', 'subject', 'group')
    search_fields = ('subject__name', 'teacher__first_name', 'teacher__last_name', 'group__group_name')
    date_hierarchy = 'class_date'


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_session', 'is_present', 'late_minutes', 'recorded_at')
    list_filter = ('is_present', 'class_session__class_date')
    search_fields = ('student__first_name', 'student__last_name', 'class_session__subject__name')
