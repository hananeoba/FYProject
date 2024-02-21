from django.shortcuts import get_object_or_404

from rest_framework import generics, mixins
from django.utils import timezone
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


# Create your views here.
class CompanyView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class CompanyDetail(generics.RetrieveAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class CompanyUpdate(generics.UpdateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    lookup_field = "pk"

    def perform_update(self, serializer):
        instance = serializer.save(
            updated_by=self.request.user, updated_at=timezone.now()
        )
        serializer.save(updated_by=self.request.user, updated_at=timezone.now())


class CompanyDelete(generics.RetrieveDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
