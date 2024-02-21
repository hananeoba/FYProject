from rest_framework import serializers
from .models import (
    AbstrctBaseModel,
    Company,
    WorkType,
    Structure,
    Installation,
    Work,
    ActivityNature,
    StructureType,
)

class AbstrctBaseModelSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    created_at = serializers.DateTimeField( read_only=True)
    class Meta:
        model = AbstrctBaseModel
        fields = "__all__"
        read_only_fields = ["created_by", "created_at"]
        abstract = True


class CompanySerializer(AbstrctBaseModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class AcivityNatureSerializer(AbstrctBaseModelSerializer):
    class Meta:
        model = ActivityNature
        fields = "__all__"


class WorkTypeSerialiser(AbstrctBaseModelSerializer):
    class Meta:
        model = WorkType
        fields = "__all__"


class StructureSerializer(AbstrctBaseModelSerializer):
    class Meta:
        model = Structure
        fields = "__all__"


class InstallationSerializer(AbstrctBaseModelSerializer):
    class Meta:
        model = Installation
        fields = "__all__"


class WorkSerializer(AbstrctBaseModelSerializer):
    class Meta:
        model = Work
        fields = "__all__"


class StructureTypeSerializer(AbstrctBaseModelSerializer):
    class Meta:
        model = StructureType
        fields = "__all__"
