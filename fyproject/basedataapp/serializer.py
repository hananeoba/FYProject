from rest_framework import serializers
from django.utils import timezone
from .models import  AbstrctBaseModel, ActivityNature, StructureType, Company, WorkType, Structure, Installation, Work

class BaseModelSerializerMixin:
    created_by = serializers.HyperlinkedRelatedField(read_only=True, view_name='user-detail', many=False)
    def set_created_fields(self, validated_data):
        user = self.context['request'].user
        validated_data['created_by'] = user
        validated_data['updated_by'] = None
        validated_data['created_at'] = timezone.now()
        validated_data['updated_at'] = None

    def set_updated_fields(self, instance, validated_data):
        user = self.context['request'].user
        validated_data['updated_by'] = user
        validated_data['updated_at'] = timezone.now()
        validated_data['created_by'] = instance.created_by
        validated_data['created_at'] = instance.created_at

class AbstrctBaseModelSerializer(serializers.ModelSerializer, BaseModelSerializerMixin):
    class Meta:
        model = AbstrctBaseModel
        fields = '__all__'
    
    def get_fields(self):
        fields = super().get_fields()

        # Make created_by and updated_by read-only
        fields['created_by'].read_only = True
        fields['updated_by'].read_only = True
        fields['created_at'].read_only = True
        fields['updated_at'].read_only = True

        return fields

    def create(self, validated_data):
        self.set_created_fields(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        self.set_updated_fields(instance, validated_data)
        return super().update(instance, validated_data)

class ActivityNatureSerializer(AbstrctBaseModelSerializer):
    class Meta(AbstrctBaseModelSerializer.Meta):
        model = ActivityNature
        fields = '__all__'
class StructureTypeSerializer(AbstrctBaseModelSerializer):
   
    class Meta(AbstrctBaseModelSerializer.Meta):
        model = StructureType
        fields = '__all__'
class CompanySerializer(AbstrctBaseModelSerializer):
    
    class Meta(AbstrctBaseModelSerializer.Meta):
        model = Company
        fields = '__all__'
class WorkTypeSerializer(AbstrctBaseModelSerializer):
    class Meta(AbstrctBaseModelSerializer.Meta):
        model = WorkType
        fields = '__all__'

class StructureSerializer(AbstrctBaseModelSerializer):
    class Meta(AbstrctBaseModelSerializer.Meta):
        model = Structure
        fields = '__all__'
class InstallationSerializer(AbstrctBaseModelSerializer):
    class Meta(AbstrctBaseModelSerializer.Meta):
        model = Installation
        fields = '__all__'
class WorkSerializer(AbstrctBaseModelSerializer):
    class Meta(AbstrctBaseModelSerializer.Meta):
        model = Work
        fields = '__all__'