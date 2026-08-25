from datetime import timedelta

from django.utils import timezone

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response

from authentication.permissions import IsAdminUserRole

from .models import (
    Event,
    EventRegistration,
)

from .serializers import (
    EventSerializer,
    EventRegistrationSerializer,
)


class EventViewSet(
    viewsets.ModelViewSet
):

    queryset = Event.objects.all().order_by(
        'event_date'
    )

    serializer_class = EventSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]

        if self.action in {'register', 'cancel_registration', 'my_registrations'}:
            return [IsAuthenticated()]

        return [IsAdminUserRole()]

    @action(
        detail=True,
        methods=['post']
    )
    def register(
        self,
        request,
        pk=None
    ):

        event = self.get_object()

        if (
            event.max_attendees
            and
            event.registrations.count()
            >= event.max_attendees
        ):

            return Response(
                {
                    "message":
                    "Event is full"
                },
                status=400
            )

        registration, created = (
            EventRegistration.objects.get_or_create(
                event=event,
                member=request.user
            )
        )

        if not created:

            return Response(
                {
                    "message":
                    "Already registered"
                }
            )

        return Response(
            {
                "message":
                "Successfully registered"
            }
        )

    @action(
        detail=True,
        methods=['post']
    )
    def cancel_registration(
        self,
        request,
        pk=None
    ):

        event = self.get_object()

        deleted, _ = (
            EventRegistration.objects.filter(
                event=event,
                member=request.user
            ).delete()
        )

        return Response(
            {
                "removed":
                deleted > 0
            }
        )

    @action(
        detail=True,
        methods=['get']
    )
    def attendees(
        self,
        request,
        pk=None
    ):

        event = self.get_object()

        registrations = (
            EventRegistration.objects.filter(
                event=event
            )
        )

        serializer = (
            EventRegistrationSerializer(
                registrations,
                many=True
            )
        )

        return Response(
            serializer.data
        )

    @action(
        detail=False,
        methods=['get']
    )
    def my_registrations(
        self,
        request
    ):

        registrations = (
            EventRegistration.objects.filter(
                member=request.user
            )
        )

        serializer = (
            EventRegistrationSerializer(
                registrations,
                many=True
            )
        )

        return Response(
            serializer.data
        )

    @action(
        detail=False,
        methods=['get']
    )
    def statistics(
        self,
        request
    ):

        total_events = (
            Event.objects.count()
        )

        upcoming_events = (
            Event.objects.filter(
                event_date__gte=timezone.now()
            ).count()
        )

        registrations = (
            EventRegistration.objects.count()
        )

        return Response(
            {
                "total_events":
                total_events,

                "upcoming_events":
                upcoming_events,

                "total_registrations":
                registrations,
            }
        )

    @action(
        detail=False,
        methods=['get']
    )
    def calendar(
        self,
        request
    ):

        events = Event.objects.all().order_by(
            'event_date'
        )

        serializer = EventSerializer(
            events,
            many=True
        )

        return Response(
            serializer.data
        )

    @action(
        detail=False,
        methods=['get']
    )
    def upcoming(
        self,
        request
    ):

        events = Event.objects.filter(
            event_date__gte=timezone.now()
        ).order_by(
            'event_date'
        )

        serializer = EventSerializer(
            events,
            many=True
        )

        return Response(
            serializer.data
        )

    @action(
        detail=False,
        methods=['get']
    )
    def today(
        self,
        request
    ):

        today = timezone.now().date()

        events = Event.objects.filter(
            event_date__date=today
        ).order_by(
            'event_date'
        )

        serializer = EventSerializer(
            events,
            many=True
        )

        return Response(
            serializer.data
        )

    @action(
        detail=False,
        methods=['get']
    )
    def this_week(
        self,
        request
    ):

        today = timezone.now()

        end_of_week = (
            today +
            timedelta(days=7)
        )

        events = Event.objects.filter(
            event_date__range=(
                today,
                end_of_week
            )
        ).order_by(
            'event_date'
        )

        serializer = EventSerializer(
            events,
            many=True
        )

        return Response(
            serializer.data
        )

    def perform_create(
        self,
        serializer
    ):
        serializer.save(
            created_by=self.request.user
        )

    def perform_update(
        self,
        serializer
    ):
        serializer.save(
            created_by=(
                serializer.instance.created_by
                if serializer.instance
                else self.request.user
            )
        )


class EventRegistrationViewSet(
    viewsets.ModelViewSet
):

    queryset = EventRegistration.objects.all()

    serializer_class = (
        EventRegistrationSerializer
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
            return EventRegistration.objects.all()

        return EventRegistration.objects.filter(
            member=self.request.user
        )

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'create', 'destroy']:
            return [IsAuthenticated()]

        return [IsAdminUserRole()]

    def perform_create(self, serializer):
        serializer.save(member=self.request.user)