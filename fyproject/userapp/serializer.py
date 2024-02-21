from rest_framework import serializers
from django.utils import timezone
from .models import User

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(read_only=True)
    updated_by = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    password = serializers.CharField(write_only=True)
   
    class Meta:
        model = User
        fields = '__all__'