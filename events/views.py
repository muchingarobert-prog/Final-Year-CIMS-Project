from datetime import timedelta

from django.utils import timezone

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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
        'start_date'
    )

    serializer_class = EventSerializer

    permission_classes = [
        IsAuthenticated
    ]

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
        detail=False,
        methods=['get']
    )
    def calendar(
        self,
        request
    ):

        events = Event.objects.all().order_by(
            'start_date'
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
            start_date__gte=timezone.now()
        ).order_by(
            'start_date'
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
            start_date__date=today
        ).order_by(
            'start_date'
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
            start_date__range=(
                today,
                end_of_week
            )
        ).order_by(
            'start_date'
        )

        serializer = EventSerializer(
            events,
            many=True
        )

        return Response(
            serializer.data
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