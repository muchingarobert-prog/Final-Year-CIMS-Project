from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    PostViewSet,
    CommentViewSet,
    PrayerRequestViewSet,
    TestimonyViewSet,
)

router = DefaultRouter()

router.register(
    'posts',
    PostViewSet
)

router.register(
    'comments',
    CommentViewSet
)

router.register(
    'prayer-requests',
    PrayerRequestViewSet
)

router.register(
    'testimonies',
    TestimonyViewSet
)

urlpatterns = [
    path(
        '',
        include(router.urls)
    ),
]