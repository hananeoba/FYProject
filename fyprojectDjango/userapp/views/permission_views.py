from django.shortcuts import get_object_or_404
from userapp.serializer import AdminPermissionSerializer
from django.contrib.auth.models import Permission

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
def PermissionOverview(request):
    api_urls = {
        "all_items": "all/",
        "Add": "create/",
        "View": "view/pk",
        "Update": "update/pk",
        "Delete": "delete/pk",
    }
    return Response(api_urls)

@permission_classes([custom_permission_generalization("adminpermission")])
@authentication_classes([JWTAuthentication])
@api_view(["GET"])
def View_Permission(request, pk):
    permission = get_object_or_404(Permission, pk=pk)
    serializer = AdminPermissionSerializer(permission)
    return Response(serializer.data)

@permission_classes([custom_permission_generalization("adminpermission")])
@authentication_classes([JWTAuthentication])
@api_view(["GET"])
def View_Permissions(request):
    permissions = Permission.objects.all()
    serializer = AdminPermissionSerializer(permissions, many=True)
    return Response(serializer.data)

@permission_classes([custom_permission_generalization("adminpermission")])
@authentication_classes([JWTAuthentication])
@api_view(["DELETE"])
def Delete_Permission(request, pk):
    permission = get_object_or_404(Permission, pk=pk)
    permission.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
