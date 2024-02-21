from rest_framework import generics, mixins
from django.utils import timezone
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


class CompanyListView(CreatedFieldsMixin, generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class CompanyDetailView(CreatedFieldsMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    lookup_field = "code"
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class StructureListView(CreatedFieldsMixin, generics.ListCreateAPIView):
    queryset = Structure.objects.all()
    serializer_class = StructureSerializer


class StructureDetailView(CreatedFieldsMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Structure.objects.all()
    serializer_class = StructureSerializer
    lookup_field = "code"


class ActivityNatureListView(CreatedFieldsMixin, generics.ListCreateAPIView):
    queryset = ActivityNature.objects.all()
    serializer_class = ActivityNatureSerializer


class ActivityNatureDetailView(
    CreatedFieldsMixin, generics.RetrieveUpdateDestroyAPIView
):
    queryset = ActivityNature.objects.all()
    serializer_class = ActivityNatureSerializer
    lookup_field = "code"


class StructureTypeListView(CreatedFieldsMixin, generics.ListCreateAPIView):
    queryset = StructureType.objects.all()
    serializer_class = StructureTypeSerializer


class StructureTypeDetailView(
    CreatedFieldsMixin, generics.RetrieveUpdateDestroyAPIView
):
    queryset = StructureType.objects.all()
    serializer_class = StructureTypeSerializer
    lookup_field = "code"


class WorkListView(CreatedFieldsMixin, generics.ListCreateAPIView):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer


class WorkDetailView(CreatedFieldsMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer
    lookup_field = "code"


class WorkTypeListView(CreatedFieldsMixin, generics.ListCreateAPIView):
    queryset = WorkType.objects.all()
    serializer_class = WorkTypeSerializer


class WorkTypeDetailView(CreatedFieldsMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = WorkType.objects.all()
    serializer_class = WorkTypeSerializer
    lookup_field = "code"


class InstallationListView(CreatedFieldsMixin, generics.ListCreateAPIView):
    queryset = Installation.objects.all()
    serializer_class = InstallationSerializer


class InstallationDetailView(CreatedFieldsMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Installation.objects.all()
    serializer_class = InstallationSerializer
    lookup_field = "code"
