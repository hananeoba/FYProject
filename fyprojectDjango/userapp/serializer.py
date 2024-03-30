from datetime import timezone
from gettext import translation
from basedataapp.models import Company, Structure
from basedataapp.serializer import  Company_Read_Serializer, Structure_Read_Serializer
from .models import AdminUser

from rest_framework import serializers

from .models import CustomPasswordValidator
from django.apps import apps
from django.db import transaction


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
class CommonUserSerializerMixin:
    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user

        with transaction.atomic():
            instance = super().create(validated_data)
        return instance

    def update(self, instance, validated_data):
        validated_data["updated_by"] = self.context["request"].user
        validated_data["updated_at"] = timezone.now()
        with transaction.atomic():
            instance = super().update(instance, validated_data)
        return instance

class UserSerializer(CommonUserSerializerMixin,serializers.ModelSerializer):
    # to remove circular import
    model_class = apps.get_model(app_label="userapp", model_name="AdminUser")

    # created_by = serializers.PrimaryKeyRelatedField(
    #     queryset=AdminUser.objects.all(),
    #     allow_null=True,
    # )
    # updated_by = serializers.PrimaryKeyRelatedField(
    #     queryset=AdminUser.objects.all(),
    #     allow_null=True,
    # )
    company = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(),
        allow_null=True,
    )
    structure = serializers.PrimaryKeyRelatedField(
        queryset=Structure.objects.all(),
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


class User_Read_Serializer(serializers.ModelSerializer):
    created_by = UserSerializer()
    updated_by = UserSerializer()
    company = Company_Read_Serializer()
    structure = Structure_Read_Serializer()
    
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


# add serializers to admingroup and permission
