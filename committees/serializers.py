from rest_framework import serializers

from .models import (
    Committee,
    CommitteePosition,
    CommitteeMembership,
)


class CommitteePositionSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = CommitteePosition

        fields = '__all__'


class CommitteeMembershipSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = CommitteeMembership

        fields = '__all__'


class CommitteeSerializer(
    serializers.ModelSerializer
):

    memberships = (
        CommitteeMembershipSerializer(
            many=True,
            read_only=True
        )
    )

    class Meta:

        model = Committee

        fields = '__all__'