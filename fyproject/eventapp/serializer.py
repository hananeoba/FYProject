from .models import Event, EventType, Causes
from rest_framework import serializers
from basedataapp.serializer import AbstrctBaseModelSerializer


class EventSerializer(AbstrctBaseModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class EventTypeSerializer(AbstrctBaseModelSerializer):
    class Meta:
        model = EventType
        fields = "__all__"


class CausesSerializer(AbstrctBaseModelSerializer):
    class Meta:
        model = Causes
        fields = "__all__"
