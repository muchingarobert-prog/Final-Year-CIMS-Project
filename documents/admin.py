from django.contrib import admin

from .models import Document


@admin.register(Document)
class DocumentAdmin(
    admin.ModelAdmin
):

    list_display = (
        'title',
        'document_type',
        'committee',
        'uploaded_by',
        'is_public',
        'created_at'
    )

    search_fields = (
        'title',
        'description'
    )

    list_filter = (
        'document_type',
        'is_public'
    )