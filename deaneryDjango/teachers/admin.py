from django.contrib import admin
from .models import Teacher


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'middle_name', 'position', 'department', 'degree', 'is_active')
    list_filter = ('department', 'position', 'is_active')
    search_fields = ('first_name', 'last_name', 'middle_name', 'email')
    date_hierarchy = 'employment_date'
