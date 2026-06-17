from django.urls import path
from . import views


urlpatterns=[


path(
'apply/<int:id>/',
views.apply_internship,
name='apply_internship'
),

path(
'my/',
views.my_applications,
name='my_applications'
),

path(
'company/',
views.company_applications,
name='company_applications'
),


path(
'accept/<int:id>/',
views.accept_application,
name='accept_application'
),


path(
'reject/<int:id>/',
views.reject_application,
name='reject_application'
),


]

