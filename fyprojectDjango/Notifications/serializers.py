from rest_framework import serializers
from .models import Notification
from userapp.models import AdminUser


class NotificationSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100),
    description = serializers.CharField(),
    date = serializers.DateTimeField(),
    users = serializers.PrimaryKeyRelatedField(queryset=AdminUser.objects.all(), many=True),
    event = serializers.PrimaryKeyRelatedField (queryset=AdminUser.objects.all()),

    class Meta:
        model = Notification
        fields = '__all__'