from rest_framework.routers import DefaultRouter

from .views import EventViewSet


router = DefaultRouter()

router.register(
    r'',
    EventViewSet
)

urlpatterns = router.urls