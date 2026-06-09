from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        'username',
        'first_name',
        'last_name',
        'email',
        'role',
        'gender',
        'is_staff',
    )

    list_filter = (
        'role',
        'gender',
        'is_staff',
        'is_superuser',
        'is_active',
    )

    search_fields = (
        'username',
        'first_name',
        'last_name',
        'email',
        'phone_number',
    )

    ordering = (
        'last_name',
        'first_name',
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            'Church Information',
            {
                'fields': (
                    'role',
                    'gender',
                    'phone_number',
                    'date_of_birth',
                    'date_of_baptism',
                    'date_of_sealing',
                )
            },
        ),
    )