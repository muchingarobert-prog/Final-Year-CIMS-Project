from django.contrib import admin
from .models import AttendanceSession, AttendanceRecord


@admin.register(AttendanceSession)
class AttendanceSessionAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'service_type',
        'session_date',
        'is_active',
    )

    search_fields = (
        'title',
    )

    list_filter = (
        'service_type',
        'is_active',
    )


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):

    list_display = (
        'member',
        'session',
        'status',
        'recorded_at',
    )

    search_fields = (
        'member__first_name',
        'member__last_name',
        'member__username',
    )

    list_filter = (
        'status',
    )