from django.contrib import admin
from .models import (
    Committee,
    CommitteePosition,
    CommitteeMembership,
)


@admin.register(Committee)
class CommitteeAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'is_active',
        'created_at',
    )

    search_fields = (
        'name',
    )

    list_filter = (
        'is_active',
    )


@admin.register(CommitteePosition)
class CommitteePositionAdmin(admin.ModelAdmin):

    list_display = (
        'title',
    )

    search_fields = (
        'title',
    )


@admin.register(CommitteeMembership)
class CommitteeMembershipAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'committee',
        'position',
        'joined_date',
        'is_active',
    )

    search_fields = (
        'user__first_name',
        'user__last_name',
        'committee__name',
    )

    list_filter = (
        'committee',
        'position',
        'is_active',
    )