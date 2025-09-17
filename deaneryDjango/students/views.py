from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from core.models import Students, Group
from .forms import StudentCreateForm, StudentEditForm
from authentication.permissions import teacher_or_admin_required, admin_required


@teacher_or_admin_required
def student_list(request):
    """Список студентов - доступ только преподавателям и администраторам"""
    students = Students.objects.all()
    
    context = {
        'students': students,
        'message': 'Список студентов'
    }
    return render(request, 'students/student_list.html', context)


@admin_required
def student_create(request):
    """Создание нового студента - доступ только администраторам"""
    if request.method == 'POST':
        form = StudentCreateForm(request.POST)
        if form.is_valid():
            student = form.save()
            messages.success(request, f'Студент {student} успешно создан!')
            return redirect('students:student_detail', student_id=student.student_id)
    else:
        form = StudentCreateForm()
    
    context = {
        'form': form,
        'title': 'Создание нового студента'
    }
    return render(request, 'students/student_create.html', context)


@admin_required
def student_edit(request, student_id):
    """Редактирование студента - доступ только администраторам"""
    student = get_object_or_404(Students, student_id=student_id)
    
    if request.method == 'POST':
        form = StudentEditForm(request.POST, instance=student)
        if form.is_valid():
            student = form.save()
            messages.success(request, f'Данные студента {student} успешно обновлены!')
            return redirect('students:student_detail', student_id=student.student_id)
    else:
        form = StudentEditForm(instance=student)
    
    context = {
        'form': form,
        'student': student,
        'title': f'Редактирование студента {student}'
    }
    return render(request, 'students/student_edit.html', context)


@teacher_or_admin_required
def student_detail(request, student_id):
    """Детальная информация о студенте"""
    try:
        student = Students.objects.get(student_id=student_id)
        context = {
            'student': student,
        }
        return render(request, 'students/student_detail.html', context)
    except Students.DoesNotExist:
        from django.http import Http404
        raise Http404("Студент не найден")


@teacher_or_admin_required
def group_detail(request, group_id):
    """Детальная информация о группе"""
    try:
        group = Group.objects.get(group_id=group_id)
        students = Students.objects.filter(group_id=group_id)
        context = {
            'group': group,
            'students': students,
        }
        return render(request, 'students/group_detail.html', context)
    except Group.DoesNotExist:
        from django.http import Http404
        raise Http404("Группа не найдена")
