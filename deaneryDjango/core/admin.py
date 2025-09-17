from django.contrib import admin
from .models import Program, Department, Semester, Subject, Group, User


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'degree_level', 'duration_years', 'is_active')
    list_filter = ('degree_level', 'is_active')
    search_fields = ('name', 'code')


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'head_teacher_id', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'code')


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('academic_year', 'semester_number', 'start_date', 'end_date', 'is_current')
    list_filter = ('semester_number', 'is_current')
    search_fields = ('academic_year',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'credits', 'department', 'is_active')
    list_filter = ('department', 'is_active')
    search_fields = ('name', 'code')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('group_name', 'course', 'program', 'admission_year', 'is_active')
    list_filter = ('course', 'program', 'is_active')
    search_fields = ('group_name',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('username', 'email')
