from django.urls import path
from . import views

urlpatterns = [
    path('', views.internship_list, name='internship_list'),
    path('create/', views.create_internship, name='create_internship'),
    path('my-applications/', views.my_applications, name='internship_my_applications'),
    path('company-dashboard/', views.company_dashboard, name='company_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-applications/', views.admin_applications, name='admin_applications'),
    path('<int:pk>/', views.internship_detail, name='internship_detail'),
    path('<int:pk>/apply/', views.apply_internship, name='apply_internship'),
    path('application/<int:pk>/<str:status>/', views.update_application_status, name='update_application_status'),
]
