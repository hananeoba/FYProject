from django.shortcuts import get_object_or_404
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from basedataapp.models import (
    Province,
    State,
    Structure,
    Structure_Type,
    Company,
    Causes,
)
from basedataapp.serializer import Structure_Serializer, Structure_Read_Serializer

from fyproject.permissions import custom_permission_generalization
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import serializers

"""-------------------------------------------STRUCTURE------------------------------------------------"""


@api_view(["GET"])
def Structure_ApiOverview(request):
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
@permission_classes([IsAuthenticated, custom_permission_generalization("structure")])
def Add_Structure(request):
    data = request.data
    state_json = data.get("state")
    company_json = data.get("company")
    province_json = data.get("province")
    parent_structure = data.get("parent_structure")
    structure_type = data.get("structure_type")

    # Validating for already existing data
    state_id = state_json.get("id")
    province_id = province_json.get("id")
    company_id = company_json.get("id")
    parent_structure_id = parent_structure.get("id")
    structure_type_id = structure_type.get("id")

    # Checking if data is valid and exists
    if (
        State.objects.filter(id=state_id).exists()
        and Province.objects.filter(id=province_id).exists()
        and Company.objects.filter(id=company_id).exists()
        and Structure.objects.filter(id=parent_structure_id).exists()
        and Structure_Type.objects.filter(id=structure_type_id).exists()
    ):
        data["state"] = state_id
        data["province"] = province_id
        data["company"] = company_id
        data["parent_structure"] = parent_structure_id
        data["structure_type"] = structure_type_id

        # Checking if Structure with the given data already exists
        if Structure.objects.filter(**data).exists():
            raise serializers.ValidationError("This data already exists")

        structure_serializer = Structure_Serializer(
            data=data, context={"request": request}
        )

        if structure_serializer.is_valid():
            structure_serializer.save()
            return Response(structure_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                structure_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["PUT"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization("structure")])
def Update_Structure(request, pk):
    structure = Structure.objects.get(pk=pk)
    data = Structure_Serializer(
        instance=structure, data=request.data, context={"request": request}
    )

    if data.is_valid():
        data.save()
        return Response(data.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization("structure")])
def View_Structure(request, pk):
    structure = Structure.objects.get(pk=pk)
    if structure:
        serializer = Structure_Read_Serializer(structure)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization("structure")])
def View_Structures(request):
    data = Structure.objects.all()
    serializer = Structure_Serializer(data, many=True)
    return Response(serializer.data)


@api_view(["DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization("structure")])
def Delete_Structure(request, pk):
    structure = get_object_or_404(Structure, pk=pk)
    structure.delete()
    return Response(status=status.HTTP_202_ACCEPTED)


"""-----------------------------------------------------------------------------------------------------"""
