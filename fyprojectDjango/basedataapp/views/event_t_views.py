from django.shortcuts import get_object_or_404
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from basedataapp.models import Event_Type
from basedataapp.serializer import Event_Type_Serializer
from fyproject.permissions import custom_permission_generalization
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import serializers

"""-------------------------------------------EVENT_TYPE------------------------------------------------"""


@api_view(["GET"])
def Event_Type_ApiOverview(request):
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
@permission_classes([IsAuthenticated, custom_permission_generalization("event_type")])
def Add_Event_Type(request):
    event_type = Event_Type_Serializer(data=request.data, context={"request": request})

    # validating for already existing data
    if Event_Type.objects.filter(**request.data).exists():
        raise serializers.ValidationError("This data already exists")

    if event_type.is_valid():
        event_type.save()
        return Response(event_type.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["PUT"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization("event_type")])
def Update_Event_Type(request, pk):
    event_type = Event_Type.objects.get(pk=pk)
    data = Event_Type_Serializer(
        instance=event_type, data=request.data, context={"request": request}
    )

    if data.is_valid():
        data.save()
        return Response(data.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization("event_type")])
def View_Event_Type(request, pk):
    event_type = Event_Type.objects.get(pk=pk)
    if event_type:
        serializer = Event_Type_Serializer(event_type)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization("event_type")])
def View_Event_Types(request):
    data = Event_Type.objects.all()
    serializer = Event_Type_Serializer(data, many=True)
    return Response(serializer.data)


@api_view(["DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization("event_type")])
def Delete_Event_Type(request, pk):
    event_type = get_object_or_404(Event_Type, pk=pk)
    event_type.delete()
    return Response(status=status.HTTP_202_ACCEPTED)


"""---------------------------------------------------------------------------------------------------------"""
