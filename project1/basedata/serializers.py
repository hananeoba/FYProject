from rest_framework import serializers
from .models import (
    Company,
    WorkType,
    Structure,
    Installation,
    Work,
    ActivityNature,
    StructureType,
)


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class AcivityNatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityNature
        fields = "__all__"


class WorkTypeSerialiser(serializers.ModelSerializer):
    class Meta:
        model = WorkType
        fields = "__all__"


class StructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Structure
        fields = "__all__"


class InstallationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Installation
        fields = "__all__"


class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = "__all__"


class StructureTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StructureType
        fields = "__all__"
