from rest_framework import viewsets

from rest_framework.decorators import action

from rest_framework.permissions import (
    IsAuthenticated
)

from rest_framework.response import Response

from authentication.permissions import (
    IsAdminUserRole,
    IsHighPrivilegeOrAbove,
)

from .models import (
    Committee,
    CommitteePosition,
    CommitteeMembership,
)

from .serializers import (
    CommitteeSerializer,
    CommitteePositionSerializer,
    CommitteeMembershipSerializer,
)


class CommitteeViewSet(
    viewsets.ModelViewSet
):

    queryset = Committee.objects.all()

    serializer_class = CommitteeSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_permissions(self):

        if self.action in [
            'create',
            'update',
            'partial_update',
            'destroy'
        ]:

            return [
                IsHighPrivilegeOrAbove()
            ]

        return [
            IsAuthenticated()
        ]

    @action(
        detail=True,
        methods=['post']
    )
    def join(
        self,
        request,
        pk=None
    ):

        committee = self.get_object()

        membership, created = (
            CommitteeMembership.objects.get_or_create(
                user=request.user,
                committee=committee
            )
        )

        if not created:

            return Response(
                {
                    "message":
                    "Already a member"
                }
            )

        return Response(
            {
                "message":
                "Successfully joined committee"
            }
        )

    @action(
        detail=True,
        methods=['delete']
    )
    def leave(
        self,
        request,
        pk=None
    ):

        committee = self.get_object()

        CommitteeMembership.objects.filter(
            user=request.user,
            committee=committee
        ).delete()

        return Response(
            {
                "message":
                "Successfully left committee"
            }
        )


class CommitteePositionViewSet(
    viewsets.ModelViewSet
):

    queryset = (
        CommitteePosition.objects.all()
    )

    serializer_class = (
        CommitteePositionSerializer
    )

    permission_classes = [
        IsAdminUserRole
    ]


class CommitteeMembershipViewSet(
    viewsets.ModelViewSet
):

    queryset = (
        CommitteeMembership.objects.all()
    )

    serializer_class = (
        CommitteeMembershipSerializer
    )

    permission_classes = [
        IsHighPrivilegeOrAbove
    ]