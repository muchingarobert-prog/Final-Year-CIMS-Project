from django.contrib import admin
from .models import Announcement


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'target_type',
        'created_by',
        'is_active',
        'created_at',
    )

    search_fields = (
        'title',
        'message',
    )

    list_filter = (
        'target_type',
        'is_active',
    )
