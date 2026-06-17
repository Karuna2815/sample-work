from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from .models import Company
from .forms import CompanyRegistrationForm


def company_register(request):
    if request.method == "POST":
        form = CompanyRegistrationForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
                return redirect('company_register')

            user = User.objects.create_user(
                username=username, email=email, password=password
            )

            company = form.save(commit=False)
            company.user = user
            company.is_approved = False
            company.save()

            messages.success(
                request,
                "Company registered! Please wait for admin approval to start posting internships."
            )
            return redirect('login')
    else:
        form = CompanyRegistrationForm()

    return render(request, 'companies/register.html', {'form': form})


@staff_member_required
def approve_company(request, id):
    company = get_object_or_404(Company, id=id)
    company.is_approved = True
    company.save()
    messages.success(request, f"{company.company_name} has been approved!")
    return redirect('admin_dashboard')
