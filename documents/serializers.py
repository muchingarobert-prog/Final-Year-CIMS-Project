from rest_framework import serializers

from .models import Document


class DocumentSerializer(
    serializers.ModelSerializer
):

    uploaded_by_name = serializers.SerializerMethodField()

    class Meta:

        model = Document

        fields = '__all__'

        read_only_fields = [
            'id',
            'uploaded_by',
            'uploaded_by_name',
            'download_count',
            'created_at',
            'updated_at',
        ]

    def get_uploaded_by_name(
        self,
        obj
    ):

        if obj.uploaded_by:

            return (
                f"{obj.uploaded_by.first_name} "
                f"{obj.uploaded_by.last_name}"
            )

        return None