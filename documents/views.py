from django.db.models import Q
from django.db.models import Count

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
    def recent(self, request):

        documents = (
            Document.objects
            .order_by('-created_at')[:20]
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
    def search(self, request):

        query = request.GET.get(
            'q',
            ''
        )

        documents = Document.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
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
    def by_type(self, request):

        document_type = request.GET.get(
            'type'
        )

        documents = Document.objects.filter(
            document_type=document_type
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

                "total_downloads":
                sum(
                    Document.objects.values_list(
                        'download_count',
                        flat=True
                    )
                ),

                "documents_by_type":
                list(
                    Document.objects
                    .values(
                        'document_type'
                    )
                    .annotate(
                        total=Count('id')
                    )
                )
            }
        )

    @action(
        detail=True,
        methods=['post']
    )
    def download(self, request, pk=None):

        document = self.get_object()

        document.download_count += 1

        document.save()

        return Response(
            {
                "message":
                "Download recorded",

                "downloads":
                document.download_count
            }
        )