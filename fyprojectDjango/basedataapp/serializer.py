from rest_framework import serializers
from django.db import transaction
from .models import (
    Activity_Nature,
    Causes,
    Company,
    Event_Type,
    Installation,
    Province,
    State,
    Structure,
    Structure_Type,
    Work_Type,
    Work,
)

# generate_new_code(): i should get this how it works?


class CommonSerializerMixin:
    def create(self, validated_data):
        new_code = self.generate_new_code()
        validated_data["code"] = new_code
        validated_data["created_by"] = self.context["request"].user

        with transaction.atomic():
            instance = super().create(validated_data)
        return instance

    def update(self, instance, validated_data):
        validated_data["updated_by"] = self.context["request"].user

        with transaction.atomic():
            instance = super().update(instance, validated_data)
        return instance


class Activity_Nature_Serializer(CommonSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Activity_Nature
        fields = "__all__"


class Causes_Serializer(CommonSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Causes
        fields = "__all__"


class Company_Serializer(CommonSerializerMixin, serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = "__all__"


class Event_Type_Serializer(CommonSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Event_Type
        fields = "__all__"


class State_Serializer(CommonSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = State
        fields = "__all__"


class Province_Serializer(CommonSerializerMixin, serializers.ModelSerializer):
    state = serializers.PrimaryKeyRelatedField(queryset=State.objects.all())

    class Meta:
        model = Province
        fields = "__all__"


# GET
class Province_Read_Serializer(serializers.ModelSerializer):
    state = State_Serializer()

    class Meta:
        model = Province
        fields = "__all__"


class Structure_Type_Serializer(CommonSerializerMixin, serializers.ModelSerializer):

    class Meta:
        model = Structure_Type
        fields = "__all__"


class Structure_Serializer(CommonSerializerMixin, serializers.ModelSerializer):
    parent_structure = serializers.PrimaryKeyRelatedField(
        queryset=Structure.objects.all(), allow_null=True, required=False
    )
    structure_type = serializers.PrimaryKeyRelatedField(
        queryset=Structure_Type.objects.all(),
        allow_null=True,
        required=False,
    )
    company = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(), allow_null=True, required=False
    )
    state = serializers.PrimaryKeyRelatedField(
        queryset=State.objects.all(), allow_null=True, required=False
    )
    province = serializers.PrimaryKeyRelatedField(
        queryset=Province.objects.all(), allow_null=True, required=False
    )

    class Meta:
        model = Structure
        fields = "__all__"


class Structure_Read_Serializer(serializers.ModelSerializer):
    company = Company_Serializer()
    parent_structure = Structure_Serializer()
    structure_type = Structure_Type_Serializer()
    state = State_Serializer()
    province = Province_Serializer()

    class Meta:
        model = Work
        fields = "__all__"


class Installation_Serializer(CommonSerializerMixin, serializers.ModelSerializer):
    structure = serializers.PrimaryKeyRelatedField(
        queryset=Structure.objects.all(), allow_null=True, required=True
    )

    class Meta:
        model = Installation
        fields = "__all__"


class Installation_Read_Serializer(serializers.ModelSerializer):
    structure = "StructureSerializer()"

    class Meta:
        model = Work
        fields = "__all__"


class Work_Type_Serializer(CommonSerializerMixin, serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(), allow_null=True, required=False
    )

    class Meta:
        model = Work
        fields = "__all__"


class Work_Type_Read_Serializer(serializers.ModelSerializer):
    company = Company_Serializer()

    class Meta:
        model = Work_Type
        fields = "__all__"


class Work_Serializer(CommonSerializerMixin, serializers.ModelSerializer):

    work_type = serializers.PrimaryKeyRelatedField(
        queryset=Work_Type.objects.all(), allow_null=True, required=False
    )
    parent_work = serializers.PrimaryKeyRelatedField(
        queryset=Work.objects.all(), allow_null=True, required=False
    )
    installation = serializers.PrimaryKeyRelatedField(
        queryset=Installation.objects.all(),
        allow_null=True,
        required=False,
    )

    class Meta:
        model = Work_Type
        fields = "__all__"


class Work_Read_Serializer(serializers.ModelSerializer):
    company = Company_Serializer()
    work_type = Work_Type_Serializer()
    parent_work = Work_Serializer()
    installation = Installation_Serializer()

    class Meta:
        model = Work
        fields = "__all__"
