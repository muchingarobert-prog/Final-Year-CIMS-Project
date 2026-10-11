from rest_framework import serializers
from pathlib import Path

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

    def validate_file(self, value):
        if value.size > 20 * 1024 * 1024:
            raise serializers.ValidationError(
                'Documents must be 20 MB or smaller.'
            )

        extension = Path(value.name).suffix.lower()
        if extension not in {
            '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
            '.txt', '.jpg', '.jpeg', '.png',
        }:
            raise serializers.ValidationError(
                'Unsupported document file type.'
            )

        if '/' in value.name or '\\' in value.name or '\x00' in value.name:
            raise serializers.ValidationError('Invalid document filename.')

        return value