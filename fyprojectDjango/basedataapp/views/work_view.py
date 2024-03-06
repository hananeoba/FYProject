from django.shortcuts import get_object_or_404
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from basedataapp.models import Installation, Work, Work_Type
from basedataapp.serializer import Work_Serializer, Work_Read_Serializer

from fyproject.permissions import custom_permission_generalization
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import serializers


"""-------------------------------------------WORK------------------------------------------------"""


@api_view(["GET"])
def Work_ApiOverview(request):
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
@permission_classes([IsAuthenticated, custom_permission_generalization("work")])
def Add_Work(request):
    data = request.data

    installation_json = data.get("installation")
    parent_work = data.get("parent_work")
    work_type = data.get("work_type")

    # Validating for already existing data
    installation_id = installation_json.get("id")
    parent_work_id = parent_work.get("id")
    work_type_id = work_type.get("id")

    # Checking if data is valid and exists
    if (
        Installation.objects.filter(id=installation_id).exists()
        and Work.objects.filter(id=parent_work_id).exists()
        and Work_Type.objects.filter(id=work_type_id).exists()
    ):
        data["installation"] = installation_id
        data["parent_Work"] = parent_work_id
        data["Work_type"] = work_type_id

        # Checking if Work with the given data already exists
        if Work.objects.filter(**data).exists():
            raise serializers.ValidationError("This data already exists")

        serializer = Work_Serializer(data=data, context={"request": request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["PUT"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization("work")])
def Update_Work(request, pk):
    work = Work.objects.get(pk=pk)
    data = Work_Serializer(
        instance=work, data=request.data, context={"request": request}
    )

    if data.is_valid():
        data.save()
        return Response(data.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization("work")])
def View_Work(request, pk):
    work = Work.objects.get(pk=pk)
    if work:
        serializer = Work_Read_Serializer(work)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization("work")])
def View_Works(request):
    data = Work.objects.all()
    serializer = Work_Read_Serializer(data, many=True)
    return Response(serializer.data)


@api_view(["DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization("work")])
def Delete_Work(request, pk):
    work = get_object_or_404(Work, pk=pk)
    work.delete()
    return Response(status=status.HTTP_202_ACCEPTED)


"""--------------------------------------------------------------------------------------------------"""
