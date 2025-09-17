from django.urls import path
from . import views

app_name = 'teachers'

urlpatterns = [
    path('', views.teacher_list, name='teacher_list'),
    path('create/', views.teacher_create, name='teacher_create'),
    path('<int:teacher_id>/', views.teacher_detail, name='teacher_detail'),
    path('<int:teacher_id>/edit/', views.teacher_edit, name='teacher_edit'),
]