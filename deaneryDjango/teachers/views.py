from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from core.models import Teachers, Department
from .forms import TeacherCreateForm, TeacherEditForm
from authentication.permissions import admin_required


@admin_required
def teacher_list(request):
    """Список преподавателей - доступ только администраторам"""
    teachers = Teachers.objects.all()
    
    context = {
        'teachers': teachers,
        'message': 'Список преподавателей'
    }
    return render(request, 'teachers/teacher_list.html', context)


@admin_required
def teacher_create(request):
    """Создание нового преподавателя - доступ только администраторам"""
    if request.method == 'POST':
        form = TeacherCreateForm(request.POST)
        if form.is_valid():
            teacher = form.save()
            messages.success(request, f'Преподаватель {teacher} успешно создан!')
            return redirect('teachers:teacher_detail', teacher_id=teacher.teacher_id)
    else:
        form = TeacherCreateForm()
    
    context = {
        'form': form,
        'title': 'Создание нового преподавателя'
    }
    return render(request, 'teachers/teacher_create.html', context)


@admin_required
def teacher_edit(request, teacher_id):
    """Редактирование преподавателя - доступ только администраторам"""
    teacher = get_object_or_404(Teachers, teacher_id=teacher_id)
    
    if request.method == 'POST':
        form = TeacherEditForm(request.POST, instance=teacher)
        if form.is_valid():
            teacher = form.save()
            messages.success(request, f'Данные преподавателя {teacher} успешно обновлены!')
            return redirect('teachers:teacher_detail', teacher_id=teacher.teacher_id)
    else:
        form = TeacherEditForm(instance=teacher)
    
    context = {
        'form': form,
        'teacher': teacher,
        'title': f'Редактирование преподавателя {teacher}'
    }
    return render(request, 'teachers/teacher_edit.html', context)


@admin_required
def teacher_detail(request, teacher_id):
    """Детальная информация о преподавателе"""
    try:
        teacher = Teachers.objects.get(teacher_id=teacher_id)
        context = {
            'teacher': teacher,
        }
        return render(request, 'teachers/teacher_detail.html', context)
    except Teachers.DoesNotExist:
        from django.http import Http404
        raise Http404("Преподаватель не найден")
