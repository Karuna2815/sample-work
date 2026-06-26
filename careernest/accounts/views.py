from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import ProfileForm
from .models import Profile, Notification
from internships.models import Internship
from applications.models import Application
from companies.models import Company


def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Account created! You can now login.")
        return redirect('login')

    return render(request, 'accounts/signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {username}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect('home')


def home(request):
    latest = Internship.objects.all().order_by('-created_at')[:6]
    companies = Company.objects.filter(is_approved=True)
    total_internships = Internship.objects.count()
    total_companies = Company.objects.filter(is_approved=True).count()
    total_applications = Application.objects.count()
    return render(request, 'accounts/home.html', {
        'latest_internships': latest,
        'companies': companies,
        'total_internships': total_internships,
        'total_companies': total_companies,
        'total_applications': total_applications,
    })


def about(request):
    return render(request, 'accounts/about.html')


def contact(request):
    if request.method == 'POST':
        messages.success(request, "Your message has been sent. We'll get back to you soon!")
        return redirect('contact')
    return render(request, 'accounts/contact.html')


@login_required
def student_dashboard(request):
    applications = Application.objects.filter(student=request.user)
    total_apps = applications.count()
    pending = applications.filter(status='Pending').count()
    accepted = applications.filter(status='Accepted').count()
    rejected = applications.filter(status='Rejected').count()
    recent = applications.order_by('-applied_date')[:5]
    applied_ids = applications.values_list('internship_id', flat=True)
    recommended = Internship.objects.exclude(id__in=applied_ids).filter(
        company__is_approved=True
    )[:4]
    return render(request, 'accounts/student_dashboard.html', {
        'total_apps': total_apps, 'pending': pending,
        'accepted': accepted, 'rejected': rejected,
        'applications': recent, 'recommended': recommended,
    })


@login_required
def mark_notification_read(request, pk):
    Notification.objects.filter(user=request.user, pk=pk).update(is_read=True)
    return redirect(request.GET.get('next', '/'))


@login_required
def mark_all_read(request):
    Notification.objects.filter(user=request.user).update(is_read=True)
    messages.success(request, "All notifications marked as read.")
    return redirect('student_dashboard')


@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'accounts/edit_profile.html', {
        'form': form
    })


@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'accounts/profile.html', {
        'profile': profile
    })
