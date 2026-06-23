from django.db import models
from django.conf import settings


class FinancialCategory(models.Model):

    CATEGORY_TYPES = [
        ('TITHE', 'Tithe'),
        ('OFFERING', 'Offering'),
        ('DONATION', 'Donation'),
        ('FUNDRAISING', 'Fundraising'),
        ('PROJECT', 'Project'),
        ('OTHER', 'Other'),
    ]

    name = models.CharField(
        max_length=100,
        unique=True
    )

    category_type = models.CharField(
        max_length=20,
        choices=CATEGORY_TYPES
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

    def __str__(self):
        return self.name


class Income(models.Model):

    PAYMENT_METHODS = [
        ('CASH', 'Cash'),
        ('MOBILE', 'Mobile Money'),
        ('BANK', 'Bank Transfer'),
        ('OTHER', 'Other'),
    ]

    member = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='income_records'
    )

    category = models.ForeignKey(
        FinancialCategory,
        on_delete=models.CASCADE,
        related_name='income_entries'
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS,
        default='CASH'
    )

    reference_number = models.CharField(
        max_length=100,
        blank=True
    )

    notes = models.TextField(
        blank=True
    )

    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='recorded_income'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.category.name} - {self.amount}"


class Expense(models.Model):

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    title = models.CharField(
        max_length=255
    )

    category = models.ForeignKey(
        FinancialCategory,
        on_delete=models.CASCADE,
        related_name='expenses'
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    description = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='requested_expenses'
    )

    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_expenses'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title