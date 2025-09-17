from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('access-denied/', views.access_denied_view, name='access_denied'),
    path('admin-panel/', views.admin_panel_view, name='admin_panel'),
]