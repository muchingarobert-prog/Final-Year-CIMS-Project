from django.contrib import admin
from .models import Committee


@admin.register(Committee)
class CommitteeAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'member_count',
    )

    search_fields = (
        'name',
    )

    ordering = (
        'name',
    )

    def member_count(self, obj):
        return obj.member_set.count()

    member_count.short_description = 'Members'