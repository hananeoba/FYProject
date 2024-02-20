from .models import Event, EventType, Causes
from rest_framework import serializers

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"

class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = "__all__"

class CausesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Causes
        fields = "__all__"
        
