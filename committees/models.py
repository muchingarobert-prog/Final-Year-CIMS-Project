from django.db import models


class Committee(models.Model):

    COMMITTEE_CHOICES = [
        ('CATERING', 'Catering Committee'),
        ('MUSIC', 'Music Committee'),
        ('ORGANIZING', 'Organizing Committee'),
        ('FINANCE', 'Finance Committee'),
        ('DRAPO', 'DRAPO Committee'),
        ('COMMUNICATION', 'Communication Committee'),
        ('TESTIFY', 'Testify Committee'),
        ('FLOWERING', 'Flowering Committee'),
        ('SECRETARIAL', 'Secretarial Committee'),
    ]

    name = models.CharField(
        max_length=50,
        unique=True,
        choices=COMMITTEE_CHOICES
    )

    description = models.TextField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.get_name_display()