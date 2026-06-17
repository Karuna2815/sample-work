from django.urls import path
from . import views

urlpatterns = [
    path(
        'register/',
        views.company_register,
        name='company_register'
    ),
    path(
        'approve/<int:id>/',
        views.approve_company,
        name='approve_company'
)
]