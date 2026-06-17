from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='company'
    )

    company_name = models.CharField(
        max_length=100
    )

    description = models.TextField()

    is_approved = models.BooleanField(
        default=False
    )


    def __str__(self):
        return self.company_name
