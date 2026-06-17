from django.db import models
from companies.models import Company


class Internship(models.Model):
    TYPE_CHOICES = [
        ('remote', 'Remote'),
        ('onsite', 'On-site'),
        ('hybrid', 'Hybrid'),
    ]

    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='internships'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    skills_required = models.CharField(max_length=500, blank=True, help_text="Comma separated skills")
    location = models.CharField(max_length=100)
    internship_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='onsite')
    duration = models.CharField(max_length=100, blank=True, help_text="e.g. 3 months")
    stipend = models.CharField(max_length=100, blank=True, help_text="e.g. Rs. 10,000/month")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
