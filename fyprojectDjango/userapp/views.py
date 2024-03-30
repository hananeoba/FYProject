"""from .models import User
from .serializer import UserSerializer, MyTokenObtainPairSerializer
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from fyproject.mixins import UserEditorPermissionMixin


from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets


# Customizing TokenObtainPairView inorder to add email to token
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserViewSet(
    UserEditorPermissionMixin,
    viewsets.ModelViewSet,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        created_fields = {
            # first time created the update fields are forced to  be none
            "created_by": (
                self.request.user if self.request.user.is_authenticated else None
            ),
            "updated_by": None,
            "created_at": timezone.now(),
            "updated_at": None,
            "password": make_password(serializer.validated_data["password"]),
        }
        serializer.save(**created_fields)

    def perform_update(self, serializer):
        updated_fields = {
            "updated_by": (
                self.request.user if self.request.user.is_authenticated else None
            ),
            "updated_at": timezone.now(),
            "password": make_password(serializer.validated_data["password"]),
        }
        serializer.save(**updated_fields)
"""

from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from userapp.utils import is_kernel
from .models import AdminUser
from .serializer import UserSerializer, User_Read_Serializer
from fyproject.permissions import custom_permission_generalization
from rest_framework import serializers
from django.core.paginator import Paginator


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([custom_permission_generalization('adminuser')])
def UserApiOverview(request):
    api_urls = {
        "all_items": "/all",
        "Add": "/",
        "View": "/view/pk",
        "Update": "/update/pk",
        "Delete": "/item/pk/delete",
    }

    return Response(api_urls)


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization("adminuser")])
def Add_User(request):
    curret_user = request.user
    data = request.data
    company_json = data.get("company")
    structure_json = data.get("structure")
    admin_groups_json = data.get("admin_groups")
    company_id = None
    structure_id = None
    admin_groups_id = []

    if company_json:
        company_id = company_json.get("id")
        data["company"] = company_id

    if structure_json:
        structure_id = structure_json.get("id")
        data["structure"] = structure_id

    if admin_groups_json:
        admin_groups_id = [admin.get("id") for admin in admin_groups_json]
        data["admin_groups"] = admin_groups_id

    user = UserSerializer(data=data, context={"request": request})

    # validating for already existing data
    if AdminUser.objects.filter(user_name=data.get("user_name")).exists():
        raise serializers.ValidationError("This data already exists")

    if user.is_valid():
        user.save()
        return Response(user.data, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND, data=user.errors)


@api_view(["PUT"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization("adminuser")])
def Update_User(request, pk):
    User = get_object_or_404(User, pk=pk)
    curret_user = request.user
    data = request.data
    company_json = data.get("company")
    structure_json = data.get("structure")
    admin_groups_json = data.get("admin_groups")
    company_id = None
    structure_id = None
    admin_groups_id = []

    if company_json and company_json != {}:
        company_id = company_json.get("id")
        data["company"] = company_id

    if structure_json:
        structure_id = structure_json.get("id")
        data["structure"] = structure_id

    if admin_groups_json:
        admin_groups_id = [admin.get("id") for admin in admin_groups_json]
        data["admin_groups"] = admin_groups_id

    user_serializer = UserSerializer(
        instance=User, data=request.data, context={"request": request}
    )

    if user_serializer.is_valid():
        user_serializer.save()
        return Response(user_serializer.data, status=status.HTTP_202_ACCEPTED)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization("adminuser")])
def View_User(request, pk):
    user = AdminUser.objects.get(pk=pk)
    if user:
        serializer = User_Read_Serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND, data= user.errors)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization("adminuser")])
def View_Users(request):
    current_user = request.user
    if is_kernel(current_user):
        user = AdminUser.objects.all()
    elif current_user.company is not None:
        user = AdminUser.objects.filter(company=current_user.company.id)
    else:
        user = AdminUser.objects.filter(id=current_user.id)
    serializer = UserReadSerializer(user, many=True) 
    return Response(serializer.data, status= status.HTTP_200_OK)


@api_view(["DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization("adminuser")])
def Delete_User(request, pk):
    user = get_object_or_404(user, pk=pk)
    user.delete()
    return Response(status=status.HTTP_202_ACCEPTED)
