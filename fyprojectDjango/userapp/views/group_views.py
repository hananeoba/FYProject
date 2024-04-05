from django.shortcuts import get_object_or_404
from userapp.serializer import AdminGroupSerializer
from userapp.models import AdminGroup

from rest_framework.response import Response
from rest_framework import status
from fyproject.permissions import custom_permission_generalization
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)

from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication


@api_view(["GET"])
def GroupApiOverview(request):
    api_urls = {
        "all_items": "all/",
        "Add": "create/",
        "View": "view/pk",
        "Update": "update/pk",
        "Delete": "delete/pk",
    }

    return Response(api_urls)


@permission_classes([custom_permission_generalization("admingroup")])
@authentication_classes([JWTAuthentication])
@api_view(["POST"])
def Add_Group(request):
    data = request.data
    permission_id = [permission.get("id") for permission in data.get("permission")]
    data["permission"]= permission_id
    serializer = AdminGroupSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([custom_permission_generalization("admingroup")])
@authentication_classes([JWTAuthentication])
@api_view(["PUT"])
def Update_Group(request, pk):
    group = get_object_or_404(AdminGroup, pk=pk)
    serializer = AdminGroupSerializer(group, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([custom_permission_generalization("admingroup")])
@authentication_classes([JWTAuthentication])
@api_view(["GET"])
def View_Group(request, pk):
    group = get_object_or_404(AdminGroup, pk=pk)
    serializer = AdminGroupSerializer(group)
    return Response(serializer.data)

@api_view(["GET"])
def View_Groups(request):
    groups = AdminGroup.objects.all()
    serializer = AdminGroupSerializer(groups, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@permission_classes([custom_permission_generalization("admingroup")])
@authentication_classes([JWTAuthentication])
@api_view(["DELETE"])
def Delete_Group(request, pk):
    group = get_object_or_404(AdminGroup, pk=pk)
    group.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
