from rest_framework import viewsets

from rest_framework.permissions import (
    IsAuthenticated
)

from rest_framework.decorators import action

from rest_framework.response import Response

from .models import Document

from .serializers import (
    DocumentSerializer
)


class DocumentViewSet(
    viewsets.ModelViewSet
):

    queryset = (
        Document.objects.all()
        .order_by('-created_at')
    )

    serializer_class = (
        DocumentSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]

    @action(
        detail=False,
        methods=['get']
    )
    def public(self, request):

        documents = Document.objects.filter(
            is_public=True
        )

        serializer = DocumentSerializer(
            documents,
            many=True
        )

        return Response(
            serializer.data
        )

    @action(
        detail=False,
        methods=['get']
    )
    def statistics(self, request):

        return Response(
            {
                "total_documents":
                Document.objects.count(),

                "public_documents":
                Document.objects.filter(
                    is_public=True
                ).count(),

                "private_documents":
                Document.objects.filter(
                    is_public=False
                ).count(),
            }
        )