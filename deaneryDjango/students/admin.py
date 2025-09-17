from django.contrib import admin
from .models import Student, Bachelor, Master, Specialist, Postgraduate


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('record_book_number', 'last_name', 'first_name', 'group_id', 'status', 'student_type', 'is_active')
    list_filter = ('status', 'student_type', 'group_id', 'is_active')
    search_fields = ('record_book_number', 'first_name', 'last_name', 'email')
    date_hierarchy = 'admission_date'


@admin.register(Bachelor)
class BachelorAdmin(admin.ModelAdmin):
    list_display = ('record_book_number', 'last_name', 'first_name', 'group_id', 'specialty_field')
    search_fields = ('record_book_number', 'first_name', 'last_name')


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ('record_book_number', 'last_name', 'first_name', 'group_id', 'research_supervisor_id')
    search_fields = ('record_book_number', 'first_name', 'last_name')


@admin.register(Specialist)
class SpecialistAdmin(admin.ModelAdmin):
    list_display = ('record_book_number', 'last_name', 'first_name', 'group_id', 'specialty_field')
    search_fields = ('record_book_number', 'first_name', 'last_name')


@admin.register(Postgraduate)
class PostgraduateAdmin(admin.ModelAdmin):
    list_display = ('record_book_number', 'last_name', 'first_name', 'group_id', 'supervisor_id')
    search_fields = ('record_book_number', 'first_name', 'last_name')
