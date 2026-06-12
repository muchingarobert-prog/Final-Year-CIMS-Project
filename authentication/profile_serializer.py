from rest_framework import serializers

from church_members.models import User


class ProfileSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = User

        exclude = [

            'password',

            'groups',

            'user_permissions',
        ]