from rest_framework import serializers

from church_members.models import User


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True
    )

    class Meta:

        model = User

        fields = [

            'username',
            'email',
            'password',

            'first_name',
            'last_name',

            'gender',
            'date_of_birth',

            'phone_number',

            'residential_address',
            'residential_apostle_area',

            'school_residential_address',

            'programme_of_study',
            'year_of_study',

            'date_of_baptism',
            'date_of_sealing',
        ]

    def create(self, validated_data):

        password = validated_data.pop(
            'password'
        )

        user = User(
            **validated_data
        )

        user.set_password(
            password
        )

        user.save()

        return user


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:

        model = User

        exclude = [

            'password',
            'groups',
            'user_permissions',
        ]