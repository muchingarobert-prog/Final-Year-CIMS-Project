from django.db import models
from committees.models import Committee

class Member(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    first_name = models.CharField(max_length=50)

    last_name = models.CharField(max_length=50)

    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES
    )

    date_of_birth = models.DateField()

    date_of_baptism = models.DateField()

    phone_number = models.CharField(max_length=20)

    email = models.EmailField(
        unique=True,
        blank=True,
        null=True
    )

    address = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"