from rest_framework.viewsets import ModelViewSet

from fyproject.mixins import EventEditorPermissionMixin
from .models import Event, EventType, Causes
from .serializer import EventSerializer, EventTypeSerializer, CausesSerializer
from basedataapp.views import CreatedFieldsMixin


class EventViewSet(EventEditorPermissionMixin, CreatedFieldsMixin, ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventTypeViewSet(EventEditorPermissionMixin, CreatedFieldsMixin, ModelViewSet):
    queryset = EventType.objects.all()
    serializer_class = EventTypeSerializer


class CausesViewSet(EventEditorPermissionMixin, CreatedFieldsMixin, ModelViewSet):
    queryset = Causes.objects.all()
    serializer_class = CausesSerializer
