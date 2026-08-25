from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from django.db.models import Q

from authentication.permissions import (
    IsAdminOrOwner,
    IsHighPrivilegeOrAbove,
)

from .models import (
    
    Post,
    Comment,
    CommentReply,
    PostReaction,
    MediaGallery,
    PrayerRequest,
    Testimony,
)

from .serializers import (
    
    PostSerializer,
    CommentSerializer,
    CommentReplySerializer,
    PostReactionSerializer,
    MediaGallerySerializer,
    PrayerRequestSerializer,
    TestimonySerializer,
)


def visible_posts_for(user):
    queryset = Post.objects.filter(is_active=True)

    if user.role in [
        'SUPER_USER',
        'ADMIN_USER',
        'HIGH_PRIVILEGE_USER'
    ]:
        return queryset

    return queryset.filter(
        Q(privacy__in=['PUBLIC', 'MEMBERS']) |
        Q(author=user)
    )


class PostViewSet(
    viewsets.ModelViewSet
):

    queryset = Post.objects.all().order_by('-created_at')

    serializer_class = (
        PostSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):
        return visible_posts_for(self.request.user).order_by('-created_at')

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]

        if self.action in ['update', 'partial_update', 'destroy', 'deactivate']:
            return [IsAdminOrOwner()]

        if self.action == 'statistics':
            return [IsHighPrivilegeOrAbove()]

        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=False,
        methods=['get']
    )
    def statistics(
        self,
        request
    ):

        return Response(
            {
                "posts":
                Post.objects.count(),

                "comments":
                Comment.objects.count(),

                "prayer_requests":
                PrayerRequest.objects.count(),

                "testimonies":
                Testimony.objects.count()
            }
        )

    @action(
        detail=True,
        methods=['post']
    )
    def deactivate(
        self,
        request,
        pk=None
    ):

        post = self.get_object()

        post.is_active = False

        post.save()

        return Response(
            {
                "message":
                "Post deactivated"
            }
        )


class CommentViewSet(
    viewsets.ModelViewSet
):

    queryset = Comment.objects.select_related('post', 'author').all()

    serializer_class = (
        CommentSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):
        return self.queryset.filter(
            post__in=visible_posts_for(self.request.user)
        )

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]

        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAdminOrOwner()]

        return [IsAuthenticated()]

    def perform_create(self, serializer):
        if serializer.validated_data['post'] not in visible_posts_for(
            self.request.user
        ):
            raise PermissionDenied('You cannot comment on this post.')

        serializer.save(author=self.request.user)

class CommentReplyViewSet(
    viewsets.ModelViewSet
):

    queryset = CommentReply.objects.select_related('comment', 'author').all()

    serializer_class = (
        CommentReplySerializer
    )

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):
        return self.queryset.filter(
            comment__post__in=visible_posts_for(self.request.user)
        )

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]

        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAdminOrOwner()]

        return [IsAuthenticated()]

    def perform_create(self, serializer):
        if serializer.validated_data['comment'].post not in visible_posts_for(
            self.request.user
        ):
            raise PermissionDenied('You cannot reply to this comment.')

        serializer.save(author=self.request.user)


class PostReactionViewSet(
    viewsets.ModelViewSet
):

    queryset = PostReaction.objects.select_related('post', 'user').all()

    serializer_class = (
        PostReactionSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):
        return self.queryset.filter(
            post__in=visible_posts_for(self.request.user)
        )

    def perform_create(self, serializer):
        if serializer.validated_data['post'] not in visible_posts_for(
            self.request.user
        ):
            raise PermissionDenied('You cannot react to this post.')

        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAdminOrOwner()]

        return [IsAuthenticated()]


class MediaGalleryViewSet(
    viewsets.ModelViewSet
):

    queryset = (
        MediaGallery.objects.all()
        .order_by('-uploaded_at')
    )

    serializer_class = (
        MediaGallerySerializer
    )

    permission_classes = [
        IsHighPrivilegeOrAbove
    ]

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

class PrayerRequestViewSet(
    viewsets.ModelViewSet
):

    queryset = (
        PrayerRequest.objects.all()
        .order_by(
            '-created_at'
        )
    )

    serializer_class = (
        PrayerRequestSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):
        if self.request.user.role in [
            'SUPER_USER',
            'ADMIN_USER',
            'HIGH_PRIVILEGE_USER'
        ]:
            return self.queryset

        return self.queryset.filter(member=self.request.user)

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]

        if self.action == 'answered':
            return [IsHighPrivilegeOrAbove()]

        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAdminOrOwner()]

        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(member=self.request.user)

    @action(
        detail=True,
        methods=['post']
    )
    def answered(
        self,
        request,
        pk=None
    ):

        prayer = self.get_object()

        prayer.is_answered = True

        prayer.save()

        return Response(
            {
                "message":
                "Prayer request marked answered"
            }
        )


class TestimonyViewSet(
    viewsets.ModelViewSet
):

    queryset = Testimony.objects.all()

    serializer_class = (
        TestimonySerializer
    )

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):
        if self.request.user.role in [
            'SUPER_USER',
            'ADMIN_USER',
            'HIGH_PRIVILEGE_USER'
        ]:
            return self.queryset

        return self.queryset.filter(
            member=self.request.user,
            approved=True
        )

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]

        if self.action == 'approve':
            return [IsHighPrivilegeOrAbove()]

        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAdminOrOwner()]

        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(member=self.request.user)

    @action(
        detail=True,
        methods=['post']
    )
    def approve(
        self,
        request,
        pk=None
    ):

        testimony = self.get_object()

        testimony.approved = True

        testimony.save()

        return Response(
            {
                "message":
                "Testimony approved"
            }
        )

    @action(
        detail=False,
        methods=['get']
    )
    def approved(
        self,
        request
    ):

        testimonies = (
            Testimony.objects.filter(
                approved=True
            )
        )

        serializer = (
            TestimonySerializer(
                testimonies,
                many=True
            )
        )

        return Response(
            serializer.data
        )