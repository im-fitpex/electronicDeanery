from django.urls import path
from . import views

app_name = 'schedule'

urlpatterns = [
    path('', views.schedule_list, name='schedule_list'),
    path('class/<int:class_id>/', views.class_detail, name='class_detail'),
    path('my-schedule/', views.my_schedule, name='my_schedule'),
]