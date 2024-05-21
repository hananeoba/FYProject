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

from basedataapp.utils import get_children_structures, get_parent_structures, generate_new_code
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
        "Delete": "/delete/pk",
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
    province_id = [province.get("id") for province in province_json]
    company_id = company_json.get("id")
    structure_type_id = structure_type.get("id")
    if parent_structure is not None:
        parent_structure_id = parent_structure.get("id")
    else:
        parent_structure_id = None
    for province in province_id:
        if not Province.objects.filter(id=province).exists():
            raise serializers.ValidationError("Province does not exist")
    # Checking if data is valid and exists
    if (
        State.objects.filter(id=state_id).exists()
        and Company.objects.filter(id=company_id).exists()
        and Structure_Type.objects.filter(id=structure_type_id).exists()
    ):
        if parent_structure_id is not None:
            if not Structure.objects.filter(id=parent_structure_id).exists():
                raise serializers.ValidationError("Parent Structure does not exist")
            else :
                data["parent_structure"] = parent_structure_id
                data["attached_parent_structure"] = True
        data["state"] = state_id
        data["province"] = province_id
        data["company"] = company_id
        data["structure_type"] = structure_type_id

        # Checking if Structure with the given data already exists
        code = generate_new_code(data.get('code')) 
        if Structure.objects.filter(code=code).exists():
            raise serializers.ValidationError("This data already exists")
    else:
        raise serializers.ValidationError("check your company , state, structure type")
    structure_serializer = Structure_Serializer(data=data, context={"request": request})
    if structure_serializer.is_valid():
        structure_serializer.save()
        return Response(structure_serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(
            data=structure_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["PUT"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization("structure")])
def Update_Structure(request, pk):
    structure = Structure.objects.get(pk=pk)
    data = request.data
    state_json = data.get("state")
    company_json = data.get("company")
    province_json = data.get("province")
    parent_structure = data.get("parent_structure")
    structure_type = data.get("structure_type")

    # Validating for already existing data
    state_id = state_json.get("id")
    province_id = [province.get("id") for province in province_json]
    company_id = company_json.get("id")
    structure_type_id = structure_type.get("id")
    if parent_structure is not None:
        parent_structure_id = parent_structure.get("id")
    else:
        parent_structure_id = None
    for province in province_id:
        if not Province.objects.filter(id=province).exists():
            raise serializers.ValidationError("Province does not exist")
    # Checking if data is valid and exists
    if (
        State.objects.filter(id=state_id).exists()
        and Company.objects.filter(id=company_id).exists()
        and Structure_Type.objects.filter(id=structure_type_id).exists()
    ):
        if parent_structure_id is not None:
            if not Structure.objects.filter(id=parent_structure_id).exists():
                raise serializers.ValidationError("Parent Structure does not exist")
            else :
                data["parent_structure"] = parent_structure_id
                data["attached_parent_structure"] = True
        data["state"] = state_id
        data["province"] = province_id
        data["company"] = company_id
        data["structure_type"] = structure_type_id
   
    serializer = Structure_Serializer(
        instance=structure, data=data, context={"request": request}
    )

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND, data=serializer.errors)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization("structure")])
def View_Structure(request, pk):
    structure = Structure.objects.get(pk=pk)
    if structure:
        serializer = Structure_Read_Serializer( structure, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization("structure")])
def View_Structures(request):
    if request.method == "GET":
        current_user = request.user
    company_id = request.query_params.get("company_id",None)

    if company_id:
        data = Structure.objects.filter(company=company_id)
    else:   
        #if is_kernel(current_user):
        data = Structure.objects.all()
        #else:
           # data = Company.objects.filter(id=current_user.company.id)

    serializer = Structure_Read_Serializer(data,context= {"request": request}, many=True)
    return Response(serializer.data , status=status.HTTP_200_OK)

@api_view(["DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization("structure")])
def Delete_Structure(request, pk):
    structure = get_object_or_404(Structure, pk=pk)
    structure.delete()
    return Response(status=status.HTTP_202_ACCEPTED, data= "Structure deleted successfully")


"""-----------------------------------------------------------------------------------------------------"""
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization("structure")])
def structure_get_parents(request):
    id= request.data.get("structure_id", None)
    structure =  get_parent_structures(id)
    serializer = Structure_Read_Serializer(structure, many=True)
    return Response(serializer.data , status=status.HTTP_200_OK)

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization("structure")])
def structure_get_children(request):
    id= request.query_params.get("structure_id", None)
    structure =  get_children_structures(id)
    serializer = Structure_Read_Serializer(structure, many=True)
    return Response(serializer.data , status=status.HTTP_200_OK)
    