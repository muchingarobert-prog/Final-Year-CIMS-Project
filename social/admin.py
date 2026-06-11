from django.contrib import admin
from .models import (
    Post,
    Comment,
    PrayerRequest,
    Testimony,
)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'author',
        'created_at',
        'is_active',
    )

    search_fields = (
        'title',
        'content',
    )

    list_filter = (
        'is_active',
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = (
        'post',
        'author',
        'created_at',
    )


@admin.register(PrayerRequest)
class PrayerRequestAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'member',
        'is_answered',
        'created_at',
    )

    list_filter = (
        'is_answered',
    )


@admin.register(Testimony)
class TestimonyAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'member',
        'approved',
        'created_at',
    )

    list_filter = (
        'approved',
    )