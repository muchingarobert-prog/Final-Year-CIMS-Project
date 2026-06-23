from django.db import models


class Visitor(models.Model):

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    FOLLOWUP_STATUS = [
        ('PENDING', 'Pending'),
        ('CONTACTED', 'Contacted'),
        ('VISITED', 'Visited'),
        ('JOINED', 'Joined'),
    ]

    first_name = models.CharField(
        max_length=100
    )

    last_name = models.CharField(
        max_length=100
    )

    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES
    )

    phone_number = models.CharField(
        max_length=30,
        blank=True
    )

    email = models.EmailField(
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    invited_by = models.CharField(
        max_length=200,
        blank=True
    )

    visit_date = models.DateField()

    follow_up_status = models.CharField(
        max_length=20,
        choices=FOLLOWUP_STATUS,
        default='PENDING'
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"