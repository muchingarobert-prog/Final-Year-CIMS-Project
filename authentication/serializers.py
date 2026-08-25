from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.password_validation import validate_password
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from rest_framework import serializers

from church_members.models import User


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )

    class Meta:

        model = User

        fields = [

            "username",
            "email",
            "password",

            "first_name",
            "last_name",

            "gender",
            "date_of_birth",

            "phone_number",

            "residential_address",
            "residential_apostle_area",

            "school_residential_address",

            "programme_of_study",
            "year_of_study",

            "date_of_baptism",
            "date_of_sealing",
        ]

    def create(self, validated_data):

        password = validated_data.pop("password")

        user = User(**validated_data)

        user.set_password(password)

        user.save()

        return user


class ProfileSerializer(serializers.ModelSerializer):

    committees = serializers.StringRelatedField(
        many=True,
        read_only=True
    )

    class Meta:

        model = User

        exclude = [

            "password",
            "groups",
            "user_permissions",
        ]

        read_only_fields = [
            "role",
            "is_staff",
            "is_superuser",
            "is_active",
        ]


class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model = User

        fields = [

            "id",
            "username",
            "first_name",
            "last_name",
            "email",

            "role",

            "gender",

            "phone_number",

            "programme_of_study",
            "year_of_study",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')

        if not request or request.user != instance:
            for field in [
                'email',
                'phone_number',
                'gender',
                'programme_of_study',
                'year_of_study',
            ]:
                data.pop(field, None)

        return data


class PasswordResetRequestSerializer(serializers.Serializer):

    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):

    uidb64 = serializers.CharField()

    token = serializers.CharField()

    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )

    def save(self):

        uid = force_str(
            urlsafe_base64_decode(
                self.validated_data["uidb64"]
            )
        )

        user = User.objects.get(pk=uid)

        token = self.validated_data["token"]

        if not PasswordResetTokenGenerator().check_token(
            user,
            token
        ):

            raise serializers.ValidationError(
                "Invalid token."
            )

        user.set_password(
            self.validated_data["password"]
        )

        user.save()

        return user