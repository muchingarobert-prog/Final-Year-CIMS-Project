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

    member_name = serializers.SerializerMethodField()

    position_name = serializers.SerializerMethodField()

    class Meta:

        model = CommitteeMembership

        fields = [
            'id',
            'user',
            'member_name',
            'committee',
            'position',
            'position_name',
            'joined_date',
            'is_active',
            'notes',
        ]

    def get_member_name(
        self,
        obj
    ):

        return (
            f"{obj.user.first_name} "
            f"{obj.user.last_name}"
        )

    def get_position_name(
        self,
        obj
    ):

        if obj.position:

            return obj.position.title

        return None


class CommitteeSerializer(
    serializers.ModelSerializer
):

    total_members = (
        serializers.SerializerMethodField()
    )

    memberships = (
        CommitteeMembershipSerializer(
            many=True,
            read_only=True
        )
    )

    class Meta:

        model = Committee

        fields = [
            'id',
            'name',
            'description',
            'purpose',
            'meeting_schedule',
            'is_active',
            'created_at',
            'updated_at',
            'total_members',
            'memberships',
        ]

    def get_total_members(
        self,
        obj
    ):

        return (
            obj.memberships.filter(
                is_active=True
            ).count()
        )