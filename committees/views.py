from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import (
    Committee,
    CommitteeMembership,
)

from .serializers import (
    CommitteeSerializer,
)


class CommitteeViewSet(
    viewsets.ModelViewSet
):

    queryset = Committee.objects.all()

    serializer_class = CommitteeSerializer

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

        if created:

            return Response(
                {
                    "message":
                    "Successfully joined committee."
                }
            )

        return Response(
            {
                "message":
                "Already a member."
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
                "Committee left successfully."
            }
        )