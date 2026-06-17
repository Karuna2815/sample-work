from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('profile/', views.profile_view, name='profile'),
    path('notifications/<int:pk>/read/', views.mark_notification_read, name='mark_read'),
    path('notifications/read-all/', views.mark_all_read, name='mark_all_read'),
]
