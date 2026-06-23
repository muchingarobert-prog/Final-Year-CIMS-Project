from django.contrib import admin

from django.urls import (
    path,
    include,
)

from django.conf import settings
from django.conf.urls.static import static


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

    path(
        'api/committees/',
        include('committees.urls')
    ),

    path(
        'api/dashboard/',
        include('dashboard.urls')
    ),

    path(
        'api/reports/',
        include('reports.urls')
    ),

    path(
        'api/finances/',
        include('finances.urls')
    ),

    path(
        'api/audit/',
        include('audit.urls')
    ),

    path(
        'api/documents/',
        include('documents.urls')
    ),

    path(
       'api/visitors/',
       include('visitors.urls')
    ),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)