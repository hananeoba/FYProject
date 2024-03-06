from django.shortcuts import get_object_or_404
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from basedataapp.models import Activity_Nature
from basedataapp.serializer import Activity_Nature_Serializer

from fyproject.permissions import custom_permission_generalization
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import serializers


"""---------------------------------------Activity_Nature_Views---------------------------------------------- """


@api_view(["GET"])
def Activity_Nature_ApiOverview(request):
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
@permission_classes(
    [IsAuthenticated, custom_permission_generalization("activity_nature")]
)
def Add_Activity_Nature(request):
    activity_nature = Activity_Nature_Serializer(
        data=request.data, context={"request": request}
    )

    # validating for already existing data
    if Activity_Nature.objects.filter(**request.data).exists():
        raise serializers.ValidationError("This data already exists")

    if activity_nature.is_valid():
        activity_nature.save()
        return Response(activity_nature.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["PUT"])
@authentication_classes([JWTAuthentication])
@permission_classes(
    [IsAuthenticated, custom_permission_generalization("activity_nature")]
)
def Update_Activity_Nature(request, pk):
    activity_nature = Activity_Nature.objects.get(pk=pk)
    data = Activity_Nature_Serializer(
        instance=activity_nature, data=request.data, context={"request": request}
    )

    if data.is_valid():
        data.save()
        return Response(data.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes(
    [IsAuthenticated, custom_permission_generalization("activity_nature")]
)
def View_Activity_Nature(request, pk):
    activity_nature = Activity_Nature.objects.get(pk=pk)
    if activity_nature:
        serializer = Activity_Nature_Serializer(activity_nature)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes(
    [IsAuthenticated, custom_permission_generalization("activity_nature")]
)
def View_Activity_Natures(request):
    # data = , ACTIVITY_NATURE_ATTS_FILTER, Activity_Nature)
    data = Activity_Nature.objects.all()
    serializer = Activity_Nature_Serializer(data, many=True)
    return Response(serializer.data)


@api_view(["DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes(
    [IsAuthenticated, custom_permission_generalization("activity_nature")]
)
def Delete_Activity_Nature(request, pk):
    activity_nature = get_object_or_404(Activity_Nature, pk=pk)
    activity_nature.delete()
    return Response(status=status.HTTP_202_ACCEPTED)


"""-------------------------------------------------------------------------------------------------"""
