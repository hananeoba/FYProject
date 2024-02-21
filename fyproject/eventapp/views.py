from rest_framework import generics, permissions
from .models import Event, EventType, Causes
from .serializer import EventSerializer, EventTypeSerializer, CausesSerializer

# Create your views here.
from basedataapp.views import CreatedFieldsMixin


class EventListView(CreatedFieldsMixin, generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventDetailView(CreatedFieldsMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = "code"
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class EventTypeListView(CreatedFieldsMixin, generics.ListCreateAPIView):
    queryset = EventType.objects.all()
    serializer_class = EventTypeSerializer


class EventTypeDetailView(CreatedFieldsMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = EventType.objects.all()
    serializer_class = EventTypeSerializer
    lookup_field = "code"
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CausesListView(CreatedFieldsMixin, generics.ListCreateAPIView):
    queryset = Causes.objects.all()
    serializer_class = CausesSerializer


class CausesDetailView(CreatedFieldsMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Causes.objects.all()
    serializer_class = CausesSerializer
    lookup_field = "code"
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
