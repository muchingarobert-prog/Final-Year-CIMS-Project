from rest_framework.routers import DefaultRouter

from .views import (
    PostViewSet,
    CommentViewSet,
    CommentReplyViewSet,
    PostReactionViewSet,
    MediaGalleryViewSet,
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
    r'replies',
    CommentReplyViewSet
)

router.register(
    r'reactions',
    PostReactionViewSet
)

router.register(
    r'gallery',
    MediaGalleryViewSet
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