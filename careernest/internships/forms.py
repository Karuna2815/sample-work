from django import forms
from .models import Internship


class InternshipForm(forms.ModelForm):
    class Meta:
        model = Internship
        fields = [
            'title', 'description', 'skills_required',
            'location', 'internship_type', 'duration', 'stipend'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'skills_required': forms.TextInput(attrs={'placeholder': 'e.g. Python, Django, React'}),
            'duration': forms.TextInput(attrs={'placeholder': 'e.g. 3 months'}),
            'stipend': forms.TextInput(attrs={'placeholder': 'e.g. Rs. 10,000/month'}),
        }
