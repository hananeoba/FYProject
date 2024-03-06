"""from rest_framework import viewsets
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


class BaseModelViewSet( CreatedFieldsMixin, viewsets.ModelViewSet
):
"""

# Base ViewSet with CreatedFieldsMixin for common functionality.
"""
# lookup_field = "code"  should it be added or no ?


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
"""

from rest_framework import serializers, status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from fyproject.permissions import custom_permission_generalization
from basedataapp.models import Company


from basedataapp.serializer import Company_Serializer


"""-------------------------------------------COMPANY------------------------------------------------"""


@api_view(["GET"])
def Company_ApiOverview(request):
    api_urls = {
        "all_items": "/all",
        "Add": "/create",
        "View": "/view/pk",
        "Update": "/update/pk",
        "Delete": "/delete/pk",
    }

    return Response(api_urls)


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization("company")])
def Add_Company(request):
    company = Company_Serializer(data=request.data, context={"request": request})

    # validating for already existing data
    if Company.objects.filter(**request.data).exists():
        raise serializers.ValidationError("This data already exists")

    if company.is_valid():
        company.save()
        return Response(company.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["PUT"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization("company")])
def Update_Company(request, pk):
    company = Company.objects.get(pk=pk)
    data = Company_Serializer(
        instance=company, data=request.data, context={"request": request}
    )

    if data.is_valid():
        data.save()
        return Response(data.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization("company")])
def View_Company(request, pk):
    company = Company.objects.get(pk=pk)
    if company:
        serializer = Company_Serializer(company)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization("company")])
def View_Companies(request):
    data = Company.objects.all()
    serializer = Company_Serializer(data, many=True)
    return Response(serializer.data)


@api_view(["DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization("company")])
def Delete_Company(request, pk):
    company = get_object_or_404(Company, pk=pk)
    company.delete()
    return Response(status=status.HTTP_202_ACCEPTED)


"""----------------------------------------------------------------------------------------------------"""
