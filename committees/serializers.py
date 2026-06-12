from rest_framework import serializers

from .models import (
    Committee,
    CommitteeMembership,
)


class CommitteeSerializer(
    serializers.ModelSerializer
):

    member_count = serializers.SerializerMethodField()

    class Meta:

        model = Committee

        fields = [
            'id',
            'name',
            'description',
            'purpose',
            'meeting_schedule',
            'is_active',
            'member_count',
        ]

    def get_member_count(
        self,
        obj
    ):
        return obj.memberships.count()


class CommitteeMembershipSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = CommitteeMembership

        fields = '__all__'