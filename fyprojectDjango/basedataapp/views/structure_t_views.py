from django.shortcuts import get_object_or_404
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from basedataapp.models import Structure_Type
from basedataapp.serializer import Structure_Type_Serializer

from fyproject.permissions import custom_permission_generalization
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import serializers

"""-------------------------------------------STRUCTURE_TYPE------------------------------------------------"""


@api_view(["GET"])
def Structure_Type_ApiOverview(request):
    api_urls = {
        "all_items": "/all",
        "Add": "/create",
        "View": "/view/pk",
        "Update": "/update/pk",
        "Delete": "/item/pk/delete",
    }

    return Response(api_urls)


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes(
    [IsAuthenticated, custom_permission_generalization("structure_type")]
)
def Add_Structure_Type(request):
    structure_type = Structure_Type_Serializer(
        data=request.data, context={"request": request}
    )

    # validating for already existing data
    if Structure_Type.objects.filter(**request.data).exists():
        raise serializers.ValidationError("This data already exists")

    if structure_type.is_valid():
        structure_type.save()
        return Response(structure_type.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["PUT"])
@authentication_classes([JWTAuthentication])
@permission_classes(
    [IsAuthenticated, custom_permission_generalization("structure_type")]
)
def Update_Structure_Type(request, pk):
    structure_type = Structure_Type.objects.get(pk=pk)
    data = Structure_Type_Serializer(
        instance=structure_type, data=request.data, context={"request": request}
    )

    if data.is_valid():
        data.save()
        return Response(data.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes(
    [IsAuthenticated, custom_permission_generalization("structure_type")]
)
def View_Structure_Type(request, pk):
    structure_type = Structure_Type.objects.get(pk=pk)
    if structure_type:
        serializer = Structure_Type_Serializer(structure_type)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes(
    [IsAuthenticated, custom_permission_generalization("structure_type")]
)
def View_Structure_Types(request):
    data = Structure_Type.objects.all()
    serializer = Structure_Type_Serializer(data, many=True)
    return Response(serializer.data)


@api_view(["DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes(
    [IsAuthenticated, custom_permission_generalization("structure_type")]
)
def Delete_Structure_Type(request, pk):
    structure_type = get_object_or_404(Structure_Type, pk=pk)
    structure_type.delete()
    return Response(status=status.HTTP_202_ACCEPTED)


"""--------------------------------------------------------------------------------------------------"""
