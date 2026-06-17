from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from internships.models import Internship
from .models import Application

@login_required(login_url='login')
def apply_internship(request, id):
    internship = get_object_or_404(Internship, id=id)

    already_applied = Application.objects.filter(
        student=request.user,
        internship=internship
    ).exists()

    if already_applied:
        return redirect('internship_detail', id=id)

    Application.objects.create(
        student=request.user,
        internship=internship
    )
    return redirect('my_applications')


@login_required(login_url='login')
def my_applications(request):
    applications = Application.objects.filter(student=request.user)
    return render(request, 'applications/my_applications.html', {
        'applications': applications
    })


@login_required(login_url='login')
def company_applications(request):
    applications = Application.objects.filter(
        internship__company=request.user.company
    )
    return render(request, 'applications/company_applications.html', {
        'applications': applications
    })


@login_required(login_url='login')
def accept_application(request, id):
    application = get_object_or_404(Application, id=id)
    application.status = "Accepted"
    application.save()
    return redirect('company_applications')


@login_required(login_url='login')
def reject_application(request, id):
    application = get_object_or_404(Application, id=id)
    application.status = "Rejected"
    application.save()
    return redirect('company_applications')
