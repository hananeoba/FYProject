from basedataapp.models import Work, Event_Type, Causes
from .models import Event
from rest_framework import serializers
from basedataapp.serializer import CommonSerializerMixin, Event_Type_Serializer, Work_Read_Serializer, Work_Serializer


class Event_Serializer(CommonSerializerMixin, serializers.ModelSerializer):
    work = serializers.PrimaryKeyRelatedField(queryset=Work.objects.all())
    event_type = serializers.PrimaryKeyRelatedField(queryset=Event_Type.objects.all())
    event_causes = serializers.PrimaryKeyRelatedField(queryset =Causes.objects.all() ,many=True)
    class Meta:
        model = Event
        fields = "__all__"

class Event_Read_Serializer(CommonSerializerMixin, serializers.ModelSerializer):
    work = Work_Serializer()
    event_type = Event_Type_Serializer()
    class Meta:
        model = Event
        fields = "__all__"
        
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
