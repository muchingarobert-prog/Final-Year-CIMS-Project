from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE_CHOICES = [
        ('SUPER_USER', 'Super User'),
        ('ADMIN_USER', 'Admin User'),
        ('HIGH_PRIVILEGE_USER', 'High Privilege User'),
        ('MEMBER', 'Member'),
    ]

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    YEAR_CHOICES = [
        ('1', 'First Year'),
        ('2', 'Second Year'),
        ('3', 'Third Year'),
        ('4', 'Fourth Year'),
        ('5', 'Fifth Year'),
        ('POSTGRAD', 'Postgraduate'),
    ]

    role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES,
        default='MEMBER'
    )

    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        blank=True
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True
    )

    residential_address = models.TextField(
        blank=True
    )

    residential_apostle_area = models.CharField(
        max_length=100,
        blank=True
    )

    school_residential_address = models.TextField(
        blank=True
    )

    date_of_baptism = models.DateField(
        null=True,
        blank=True
    )

    date_of_sealing = models.DateField(
        null=True,
        blank=True
    )

    programme_of_study = models.CharField(
        max_length=200,
        blank=True
    )

    year_of_study = models.CharField(
        max_length=20,
        choices=YEAR_CHOICES,
        blank=True
    )

    church_role_description = models.TextField(
        blank=True
    )

    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True
    )

    bio = models.TextField(
        blank=True
    )

    interests_and_skills = models.TextField(
        blank=True
    )

    is_profile_public = models.BooleanField(
        default=False
    )

    receive_notifications = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"