from django.shortcuts import get_object_or_404
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from basedataapp.models import Causes, Event_Type
from basedataapp.serializer import Causes_Serializer

from fyproject.permissions import custom_permission_generalization
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import serializers

"""-------------------------------------------CAUSE---------------------------------------------"""


@api_view(["GET"])
def Cause_ApiOverview(request):
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
@permission_classes([IsAuthenticated, custom_permission_generalization("causes")])
def Add_Cause(request):
    try:
        data = request.data
        event_type = data.get("event_type")
        event_type = Event_Type.objects.get(id=event_type)
        data["company"] = event_type.company.id
        cause = Causes_Serializer(data=request.data, context={"request": request})
        if cause.is_valid():
            # Check if the data already exists
            if Causes.objects.filter(**request.data).exists():
                return Response(
                    {"detail": "This data already exists"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            cause.save()
            return Response(cause.data, status=status.HTTP_201_CREATED)
        else:
            print(cause.errors)
            return Response(cause.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(str(e))


@api_view(["PUT"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization("cause")])
def Update_Cause(request, pk):
    causes = Causes.objects.get(pk=pk)
    data = Causes_Serializer(
        instance=causes, data=request.data, context={"request": request}
    )

    if data.is_valid():
        data.save()
        return Response(data.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization("causes")])
def View_Cause(request, pk):
    causes = Causes.objects.get(pk=pk)
    if causes:
        serializer = Causes_Serializer(causes)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization("causes")])
def View_Causes(request):
    try:
        current_user = request.user
        event_type = request.query_params.get("event_type", None)
        event_sub_type = request.query_params.get("event_sub_type", None)
        if event_type:
            causes = Causes.objects.filter(event_type=event_type)
        elif event_sub_type:
            causes = Causes.objects.filter(event_sub_type=event_sub_type)
        else:
            if is_kernel(current_user):
                causes = Causes.objects.all()
            else:
                causes = Causes.objects.filter(company=current_user.company)
        if causes:
            serializer = Causes_Serializer(causes, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(str(e))


@api_view(["DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization("causes")])
def Delete_Cause(request, pk):
    causes = get_object_or_404(Causes, pk=pk)
    causes.delete()
    return Response(status=status.HTTP_202_ACCEPTED)


"""---------------------------------------------------------------------------------------------"""
