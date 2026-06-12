from rest_framework.routers import DefaultRouter

from .views import (
    PostViewSet,
    CommentViewSet,
    PrayerRequestViewSet,
    TestimonyViewSet,
)

router = DefaultRouter()

router.register(
    r'posts',
    PostViewSet
)

router.register(
    r'comments',
    CommentViewSet
)

router.register(
    r'prayer-requests',
    PrayerRequestViewSet
)

router.register(
    r'testimonies',
    TestimonyViewSet
)

urlpatterns = router.urls