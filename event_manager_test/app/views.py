"""Endpoint's views."""
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from event_manager_test.app.models import Event
from event_manager_test.app.filters import EventFilter
from event_manager_test.app.serializers import (
    SignUpSerializer, EventSerializer
)
from event_manager_test.utils.exceptions.event import MustBeTheOwnerError


class SignUpView(CreateAPIView):
    """Sign up new user view."""
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer


class EventViewSet(ModelViewSet):
    """"List, get, create, update and delete event view set."""
    permission_classes = (IsAuthenticated, )
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    filter_backends = (EventFilter, )

    def is_owner(self, raise_exception=False) -> bool:
        """
        Method that check if who's doing any request is the
        actual owner of the event.

        Accept a `raise_exception` parameter (boolean) that will raise
        an exception in case it is not the owner, otherwise returns a boolean.
        """
        is_owner = self.request.user.id == self.get_object().owner.id

        if not is_owner and raise_exception:
            raise MustBeTheOwnerError()

        return is_owner

    def create(self, request):
        """
        Create event method.

        Overridden to use a deterministic way of retrieving the user.
        Only the logged account that is sending this request can be
        the owner of the event.
        """
        request.data.update({'owner': request.user.id})
        return super().create(request)

    def update(self, request, pk=None, partial=False):
        """
        Update event method.

        Overridden to double check that who is doing the action is
        the actual owner of the event.
        """
        self.is_owner(raise_exception=True)

        return super().update(request, pk, partial=partial)

    def partial_update(self, request, pk=None):
        """
        Partial update event method.

        Built-in partial_update method uses kwargs with key 'Partial'
        that throws an error over this key.

        Quickly solved by overriding and giving the update method the key
        parameter it expects ('partial').
        """
        return self.update(request, pk=pk, partial=True)

    def destroy(self, request, pk=None):
        """
        Update event method.

        Overridden to double check that who is doing the action is
        the actual owner of the event.
        """
        self.is_owner(raise_exception=True)

        return super().destroy(request, pk)

    @action(detail=True, methods=['patch'])
    def register(self, request, pk):
        serializer = EventSerializer(
            instance=self.get_object(),
            data={},
            context={
                'add_user': request.user.id
            },
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response("You have been registered.")

    @action(detail=True, methods=['patch'])
    def deregister(self, request, pk):
        serializer = EventSerializer(
            instance=self.get_object(),
            data={},
            context={
                'remove_user': request.user.id
            },
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response("You have been de-registered.")
