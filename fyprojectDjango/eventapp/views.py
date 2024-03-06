from django.shortcuts import get_object_or_404
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from basedataapp.models import Work, Event_Type

from .models import Event
from .serializer import Event_Serializer, Event_Read_Serializer
from fyproject.permissions import custom_permission_generalization
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import serializers


"""-------------------------------------------EVENT------------------------------------------------"""


@api_view(["GET"])
def Event_ApiOverview(request):
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
@permission_classes([IsAuthenticated, custom_permission_generalization("event")])
def Add_Event(request):
    data = request.data

    work_json = data.get("work")
    event_type = data.get("event_type")

    # Validating for already existing data
    work_id = work_json.get("id")
    event_type_id = event_type.get("id")

    # Checking if data is valid and exists
    if (
        Work.objects.filter(id=work_id).exists()
        and Event_Type.objects.filter(id=event_type_id).exists()
    ):
        data["work"] = work_id
        data["event_type"] = event_type_id

        # Checking if event with the given data already exists
        if Event.objects.filter(**data).exists():
            raise serializers.ValidationError("This data already exists")

        serializer = Event_Serializer(data=data, context={"request": request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["PUT"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization("event")])
def Update_Event(request, pk):
    event = event.objects.get(pk=pk)
    data = Event_Serializer(
        instance=event, data=request.data, context={"request": request}
    )

    if data.is_valid():
        data.save()
        return Response(data.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization("event")])
def View_Event(request, pk):
    event = Event.objects.get(pk=pk)
    if event:
        serializer = Event_Read_Serializer(event)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization("event")])
def View_Events(request):
    selectedInstallation_json = request.query_param.get("selectedInstallation")
    selected_installation_id = selectedInstallation_json.get("id")
    work = Work.objects.filter(installation=selected_installation_id)
    data = Event.objects.filter(work=work)
    serializer = Event_Read_Serializer(data, many=True)
    return Response(serializer.data)


@api_view(["DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization("event")])
def Delete_Event(request, pk):
    event = get_object_or_404(event, pk=pk)
    event.delete()
    return Response(status=status.HTTP_202_ACCEPTED)


"""--------------------------------------------------------------------------------------------------"""
