from rest_framework.routers import (
    DefaultRouter
)

from .views import (
    CommitteeViewSet,
    CommitteePositionViewSet,
    CommitteeMembershipViewSet,
)

router = DefaultRouter()

router.register(
    r'',
    CommitteeViewSet,
    basename='committees'
)

router.register(
    r'positions',
    CommitteePositionViewSet
)

router.register(
    r'memberships',
    CommitteeMembershipViewSet
)

urlpatterns = router.urls