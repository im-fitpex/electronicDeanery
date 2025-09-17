from django.contrib import admin
from .models import Grade


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'value', 'exam_date', 'teacher', 'control_type')
    list_filter = ('value', 'control_type', 'semester', 'subject')
    search_fields = ('student__first_name', 'student__last_name', 'student__record_book_number', 'subject__name')
    date_hierarchy = 'exam_date'
