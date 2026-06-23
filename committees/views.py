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

    @action(
        detail=True,
        methods=['get']
    )
    def members(
        self,
        request,
        pk=None
    ):

        committee = self.get_object()

        memberships = (
            CommitteeMembership.objects.filter(
                committee=committee,
                is_active=True
            )
        )

        serializer = (
            CommitteeMembershipSerializer(
                memberships,
                many=True
            )
        )

        return Response(
            serializer.data
        )

    @action(
        detail=True,
        methods=['get']
    )
    def leadership(
        self,
        request,
        pk=None
    ):

        committee = self.get_object()

        leaders = (
            CommitteeMembership.objects.filter(
                committee=committee,
                position__isnull=False,
                is_active=True
            )
        )

        serializer = (
            CommitteeMembershipSerializer(
                leaders,
                many=True
            )
        )

        return Response(
            serializer.data
        )

    @action(
        detail=False,
        methods=['get']
    )
    def analytics(
        self,
        request
    ):

        committees = Committee.objects.all()

        data = []

        for committee in committees:

            data.append(
                {
                    "id":
                    committee.id,

                    "name":
                    committee.name,

                    "members":
                    committee.memberships.filter(
                        is_active=True
                    ).count(),

                    "active":
                    committee.is_active,

                    "meeting_schedule":
                    committee.meeting_schedule,
                }
            )

        return Response(
            data
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

    @action(
        detail=True,
        methods=['post']
    )
    def deactivate(
        self,
        request,
        pk=None
    ):

        membership = self.get_object()

        membership.is_active = False

        membership.save()

        return Response(
            {
                "message":
                "Membership deactivated"
            }
        )

    @action(
        detail=True,
        methods=['post']
    )
    def activate(
        self,
        request,
        pk=None
    ):

        membership = self.get_object()

        membership.is_active = True

        membership.save()

        return Response(
            {
                "message":
                "Membership activated"
            }
        )