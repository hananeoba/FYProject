from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from django.utils import timezone
from fyproject.mixins import BaseEditorPermissionMixin
from rest_framework import permissions
from .models import (
    Company,
    WorkType,
    Structure,
    Installation,
    Work,
    ActivityNature,
    StructureType,
)

from .serializer import (
    CompanySerializer,
    ActivityNatureSerializer,
    WorkTypeSerializer,
    StructureSerializer,
    InstallationSerializer,
    WorkSerializer,
    StructureTypeSerializer,
)


class CreatedFieldsMixin:
    def perform_create(self, serializer):
        created_fields = {
            "created_by": (
                self.request.user if self.request.user.is_authenticated else None
            ),
            "updated_by": None,
            "created_at": timezone.now(),
            "updated_at": None,
        }
        serializer.save(**created_fields)

    def perform_update(self, serializer):
        updated_fields = {
            "updated_by": (
                self.request.user if self.request.user.is_authenticated else None
            ),
            "updated_at": timezone.now(),
        }
        serializer.save(**updated_fields)


class BaseModelViewSet(
    BaseEditorPermissionMixin, CreatedFieldsMixin, viewsets.ModelViewSet
):
    """
    Base ViewSet with CreatedFieldsMixin for common functionality.
    """

    lookup_field = "code"


class CompanyViewSet(
    BaseModelViewSet,
):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class StructureViewSet(BaseModelViewSet):
    queryset = Structure.objects.all()
    serializer_class = StructureSerializer


class ActivityNatureViewSet(BaseModelViewSet):
    queryset = ActivityNature.objects.all()
    serializer_class = ActivityNatureSerializer


class StructureTypeViewSet(BaseModelViewSet):
    queryset = StructureType.objects.all()
    serializer_class = StructureTypeSerializer


class WorkViewSet(BaseModelViewSet):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer


class WorkTypeViewSet(BaseModelViewSet):
    queryset = WorkType.objects.all()
    serializer_class = WorkTypeSerializer


class InstallationViewSet(BaseModelViewSet):
    queryset = Installation.objects.all()
    serializer_class = InstallationSerializer
