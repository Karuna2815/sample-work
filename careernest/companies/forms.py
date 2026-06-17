from django import forms
from .models import Company


class CompanyRegistrationForm(forms.ModelForm):

    username = forms.CharField(
        max_length=150
    )

    email = forms.EmailField()

    password = forms.CharField(
        widget=forms.PasswordInput
    )


    class Meta:

        model = Company

        fields = [
            'company_name',
            'description'
        ]