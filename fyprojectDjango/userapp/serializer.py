from .models import AdminUser

from rest_framework import serializers
from rest_framework.serializers import ValidationError

from .models import  CustomPasswordValidator
from django.apps import apps




"""
# Customizing TokenObtainPairSerializer inorder to add email to token

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["email"] = user.email #add email to token
        # ...

        return token

"""


class UserSerializer(serializers.ModelSerializer):
    model_class = apps.get_model(app_label='userapp',model_name= 'AdminUser')

    created_by = serializers.PrimaryKeyRelatedField(
        queryset=AdminUser.objects.all(),
        allow_null=True,
    )
    updated_by = serializers.PrimaryKeyRelatedField(
        queryset=AdminUser.objects.all(),
        allow_null=True,
    )
    password = serializers.CharField(
        write_only=True,
        validators=[CustomPasswordValidator()],
        style={"input_type": "password"},
    )

    class Meta:
        model = AdminUser
        fields = "__all__"

    def create(self, validated_data):
        user = AdminUser.objects.create_user(**validated_data)
        return user


class UserReadSerializer(serializers.ModelSerializer):
    created_by = UserSerializer()
    updated_by = UserSerializer()

    class Meta:
        model = AdminUser
        fields = "__all__"
        extra_kwargs = (
            {  # to make password write_only and automatically set audit fields
                "password": {"write_only": True},
                "created_at": {"read_only": True},
                "updated_at": {"read_only": True},
            }
        )
