from django.contrib import admin
from django.urls import (
    path,
    include,
)

urlpatterns = [

    path(
        'admin/',
        admin.site.urls
    ),

    path(
        'api/auth/',
        include('authentication.urls')
    ),

    path(
        'api/attendance/',
        include('attendance.urls')
    ),

    path(
        'api/events/',
        include('events.urls')
    ),

    path(
        'api/users/',
        include('church_members.urls')
    ),

    path(
        'api/notifications/',
        include('notifications.urls')
    ),

    path(
        'api/social/',
        include('social.urls')
    ),

    path(
        'api/announcements/',
        include('announcements.urls')
    ),
]