from rest_framework import serializers
from django.utils import timezone
from .models import User

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# Customizing TokenObtainPairSerializer inorder to add email to token
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["email"] = user.email #add email to token
        # ...

        return token


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {#to make password write_only and automatically set audit fields
            "password": {"write_only": True},
            "created_by": {"read_only": True},
            "updated_by": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }
