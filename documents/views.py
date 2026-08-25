from django.db.models import Q
from django.db.models import Count

from rest_framework import viewsets

from rest_framework.permissions import (
    IsAuthenticated,
    SAFE_METHODS,
)

from rest_framework.decorators import action

from rest_framework.response import Response

from authentication.permissions import IsAdminOrOwner

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

    def get_queryset(self):
        queryset = Document.objects.order_by('-created_at')

        if self.request.user.role in [
            'SUPER_USER',
            'ADMIN_USER',
            'HIGH_PRIVILEGE_USER'
        ]:
            return queryset

        return queryset.filter(
            Q(is_public=True) |
            Q(uploaded_by=self.request.user)
        )

    def get_permissions(self):
        if self.request.method in SAFE_METHODS or self.action == 'create':
            return [IsAuthenticated()]

        return [IsAdminOrOwner()]

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

    @action(
        detail=False,
        methods=['get']
    )
    def public(self, request):

        documents = self.get_queryset().filter(is_public=True)

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

        documents = self.get_queryset()[:20]

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

        documents = self.get_queryset().filter(
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

        documents = self.get_queryset().filter(
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
                self.get_queryset().count(),

                "public_documents":
                self.get_queryset().filter(is_public=True).count(),

                "private_documents":
                self.get_queryset().filter(is_public=False).count(),

                "total_downloads":
                sum(
                    self.get_queryset().values_list(
                        'download_count',
                        flat=True
                    )
                ),

                "documents_by_type":
                list(
                    self.get_queryset()
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