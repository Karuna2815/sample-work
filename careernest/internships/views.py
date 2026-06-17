from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Internship
from applications.models import Application
from companies.models import Company
from .forms import InternshipForm


def internship_list(request):
    internships = Internship.objects.all()
    query = request.GET.get('q')
    location = request.GET.get('location')
    company = request.GET.get('company')
    skills = request.GET.get('skills')
    internship_type = request.GET.get('type')

    if query:
        internships = internships.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(skills_required__icontains=query)
        )

    if location:
        internships = internships.filter(location__iexact=location)

    if company:
        internships = internships.filter(company__company_name__icontains=company)

    if skills:
        internships = internships.filter(skills_required__icontains=skills)

    if internship_type:
        internships = internships.filter(internship_type=internship_type)

    locations = Internship.objects.values_list('location', flat=True).distinct().order_by('location')
    companies_list = Company.objects.filter(is_approved=True).values_list('company_name', flat=True).order_by('company_name')

    return render(request, 'internships/list.html', {
        'internships': internships,
        'query': query,
        'location': location,
        'company': company,
        'skills': skills,
        'internship_type': internship_type,
        'locations': locations,
        'companies_list': companies_list,
    })


def internship_detail(request, pk):
    internship = get_object_or_404(Internship, pk=pk)
    has_applied = False
    if request.user.is_authenticated:
        has_applied = Application.objects.filter(
            student=request.user, internship=internship
        ).exists()
    skills_list = [s.strip() for s in internship.skills_required.split(',') if s.strip()]
    return render(request, 'internships/detail.html', {
        'internship': internship,
        'has_applied': has_applied,
        'skills_list': skills_list,
    })


@login_required
def apply_internship(request, pk):
    internship = get_object_or_404(Internship, pk=pk)

    if Application.objects.filter(student=request.user, internship=internship).exists():
        messages.warning(request, "You have already applied for this internship.")
        return redirect('internship_detail', pk=pk)

    Application.objects.create(student=request.user, internship=internship)
    messages.success(request, "Applied successfully!")
    return redirect('internship_detail', pk=pk)


@login_required
def my_applications(request):
    applications = Application.objects.filter(student=request.user)
    return render(request, 'internships/my_applications.html', {
        'applications': applications
    })


def company_check(user):
    return hasattr(user, 'company')


@login_required
@user_passes_test(company_check)
def create_internship(request):
    company = request.user.company

    if not company.is_approved:
        messages.warning(request, "Your company is not yet approved by admin.")
        return redirect('company_dashboard')

    if request.method == "POST":
        form = InternshipForm(request.POST)
        if form.is_valid():
            internship = form.save(commit=False)
            internship.company = company
            internship.save()
            messages.success(request, "Internship posted successfully!")
            return redirect('internship_list')
    else:
        form = InternshipForm()

    return render(request, 'internships/create_internship.html', {'form': form})


@login_required
@user_passes_test(company_check)
def company_dashboard(request):
    company = request.user.company
    internships = Internship.objects.filter(company=company)
    applications = Application.objects.filter(internship__in=internships)
    total_apps = applications.count()
    pending = applications.filter(status='Pending').count()
    accepted = applications.filter(status='Accepted').count()

    return render(request, 'internships/company_dashboard.html', {
        'internships': internships,
        'applications': applications,
        'total_apps': total_apps,
        'pending': pending,
        'accepted': accepted,
    })


@login_required
@user_passes_test(company_check)
def update_application_status(request, pk, status):
    application = get_object_or_404(Application, pk=pk)
    if status in ['Accepted', 'Rejected']:
        application.status = status
        application.save()
        messages.success(request, f"Application {status.lower()}.")
    return redirect('company_dashboard')


@staff_member_required
def admin_applications(request):
    applications = Application.objects.all()
    return render(request, 'internships/admin_applications.html', {
        'applications': applications
    })


@staff_member_required
def admin_dashboard(request):
    total_students = User.objects.count()
    total_internships = Internship.objects.count()
    total_applications = Application.objects.count()
    companies = Company.objects.all()

    return render(request, 'internships/admin_dashboard.html', {
        'total_students': total_students,
        'total_internships': total_internships,
        'total_applications': total_applications,
        'companies': companies,
    })
