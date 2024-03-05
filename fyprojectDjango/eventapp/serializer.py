from .models import Event
from rest_framework import serializers
from basedataapp.serializer import CommonSerializerMixin


class EventSerializer(CommonSerializerMixin):
    class Meta:
        model = Event
        fields = "__all__"


