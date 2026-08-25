from rest_framework.routers import (
    DefaultRouter
)

from .views import (
    EventViewSet,
    EventRegistrationViewSet,
)

router = DefaultRouter()

router.register(
    r'registrations',
    EventRegistrationViewSet
)

router.register(
    r'',
    EventViewSet,
    basename='events'
)

urlpatterns = router.urls