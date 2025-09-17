from django.urls import path
from . import views

app_name = 'grades'

urlpatterns = [
    path('', views.grade_list, name='grade_list'),
    path('student/<int:student_id>/', views.student_grades, name='student_grades'),
    path('my-grades/', views.my_grades, name='my_grades'),
]