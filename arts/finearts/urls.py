from django.urls import path
from finearts import views

urlpatterns = [
    path('', views.register_view, name='register'),
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('user_profile/', views.user_profile_view, name='user_profile'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('staff_register/', views.staff_register_view, name='staff_register'),
    path('staff_login/', views.staff_login_view, name='staff_login'),
    path('teachers/', views.teachers_view, name='teachers'),
    path('accept_event/', views.accept_event, name='accept_event'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('upload_results/', views.upload_results, name='upload_results'),
    path('submit_results/', views.submit_results, name='submit_results'),



]