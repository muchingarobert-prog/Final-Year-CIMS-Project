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

    queryset = Event.objects.all()

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
                    "Already registered."
                }
            )

        return Response(
            {
                "message":
                "Successfully registered."
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

        events = Event.objects.filter(
            is_active=True
        )

        serializer = EventSerializer(
            events,
            many=True
        )

        return Response(
            serializer.data
        )