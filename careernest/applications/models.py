from django.db import models
from django.contrib.auth.models import User
from internships.models import Internship


class Application(models.Model):

    STATUS_CHOICES = [
        ('Pending','Pending'),
        ('Accepted','Accepted'),
        ('Rejected','Rejected'),
    ]


    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='applications'
    )


    internship = models.ForeignKey(
        Internship,
        on_delete=models.CASCADE,
        related_name='applications'
    )


    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )


    applied_date = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return self.student.username