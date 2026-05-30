from django.contrib import admin
from .models import Member


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'gender',
        'phone_number',
        'email',
        'date_of_baptism',
    )

    search_fields = (
        'first_name',
        'last_name',
        'phone_number',
        'email',
    )

    list_filter = (
        'gender',
        'date_of_baptism',
    )

    ordering = (
        'last_name',
        'first_name',
    )