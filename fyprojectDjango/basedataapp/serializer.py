from rest_framework import serializers
from django.utils import timezone
from .models import (
    AbstrctBaseModel,
    ActivityNature,
    StructureType,
    Company,
    WorkType,
    Structure,
    Installation,
    Work,
)


class AbstrctBaseModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbstrctBaseModel
        fields = "__all__"

    def get_fields(self):
        fields = super().get_fields()

        # Make created_by and updated_by read-only
        fields["created_by"].read_only = True
        fields["updated_by"].read_only = True
        fields["created_at"].read_only = True
        fields["updated_at"].read_only = True

        return fields


class ActivityNatureSerializer(AbstrctBaseModelSerializer):
    class Meta:
        model = ActivityNature
        fields = "__all__"


class StructureTypeSerializer(AbstrctBaseModelSerializer):

    class Meta:
        model = StructureType
        fields = "__all__"


class CompanySerializer(AbstrctBaseModelSerializer):

    class Meta:
        model = Company
        fields = "__all__"


class WorkTypeSerializer(AbstrctBaseModelSerializer):
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