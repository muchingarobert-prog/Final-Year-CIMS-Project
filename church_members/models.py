from PIL import Image

from django.contrib.auth.models import AbstractUser
from django.db import models

from committees.models import Committee


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

    email = models.EmailField(
        unique=True
    )

    date_of_birth = models.DateField(
        null=True,
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

    programme_of_study = models.CharField(
        max_length=100,
        blank=True
    )

    year_of_study = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    committees = models.ManyToManyField(
        Committee,
        blank=True,
        related_name='members'
    )

    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True
    )

    bio = models.TextField(
        blank=True
    )

    church_role_description = models.CharField(
        max_length=255,
        blank=True
    )

    interests_and_skills = models.TextField(
        blank=True
    )

    is_profile_public = models.BooleanField(
        default=True
    )

    receive_notifications = models.BooleanField(
        default=True
    )

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

        if self.profile_picture:

            image = Image.open(
                self.profile_picture.path
            )

            image = image.convert("RGB")

            image.thumbnail(
                (300, 300)
            )

            image.save(
                self.profile_picture.path,
                optimize=True,
                quality=85
            )

    def __str__(self):

        return (
            f"{self.first_name} {self.last_name}"
        )