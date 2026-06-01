from django.contrib import admin
from .models import AttendanceSession, AttendanceRecord


@admin.register(AttendanceSession)
class AttendanceSessionAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'service_type',
        'session_date',
    )

    list_filter = (
        'service_type',
        'session_date',
    )

    search_fields = (
        'title',
    )

    ordering = (
        '-session_date',
    )


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):

    list_display = (
        'member',
        'session',
        'status',
    )

    list_filter = (
        'status',
        'session',
    )

    search_fields = (
        'member__first_name',
        'member__last_name',
    )