from rest_framework import serializers
from .models import Notification, Notification_User
from userapp.models import AdminUser
from userapp.serializer import UserSerializer


class NotificationSerializer(serializers.ModelSerializer):
    title = (serializers.CharField(max_length=100),)
    description = (serializers.CharField(),)
    date = (serializers.DateTimeField(),)

    users = (
        serializers.PrimaryKeyRelatedField(queryset=AdminUser.objects.all(), many=True),
    )
    event = (serializers.PrimaryKeyRelatedField(queryset=AdminUser.objects.all()),)

    class Meta:
        model = Notification
        fields = "__all__"


class NotificationUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Notification_User
        fields = "__all__"


class NotificationSerializer(serializers.ModelSerializer):
    title = (serializers.CharField(max_length=100),)
    description = (serializers.CharField(),)
    date = (serializers.DateTimeField(),)
    users = (NotificationUserSerializer(many=True, read_only=True),)
    event = (serializers.PrimaryKeyRelatedField(queryset=AdminUser.objects.all()),)

    class Meta:
        model = Notification
        fields = "__all__"
