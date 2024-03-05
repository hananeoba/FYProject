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
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import AdminUser
from .serializer import UserSerializer, UserReadSerializer
from fyproject.permissions import custom_permission_generalization
from rest_framework import serializers
from django.core.paginator import Paginator



@api_view(['GET'])
#@authentication_classes([JWTAuthentication])
#@permission_classes([custom_permission_generalization('adminuser')])
def UserApiOverview(request):
    api_urls = {
        'all_items': '/all',
        'Add': '/',
        'View': '/view/pk',
        'Update': '/update/pk',
        'Delete': '/item/pk/delete'
    }

    return Response(api_urls)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization('adminuser')])
def Add_User(request):
    user = UserSerializer(data=request.data, context={'request': request})

    # validating for already existing data
    if AdminUser.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')

    if user.is_valid():
        user.save()
        return Response(user.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
#@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization('adminuser')])
def Update_User(request, pk):
    User = get_object_or_404(User, pk=pk)
    data = UserSerializer(instance=User, data=request.data, context={'request': request})

    if data.is_valid():
        data.save()
        return Response(data.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
#@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization('adminuser')])
def View_User(request, pk):
    user =AdminUser.objects.get(pk=pk)
    if user:
        serializer = UserReadSerializer(user)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
#@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization('adminuser')])
def View_Users(request):
    user = AdminUser.objects.all()
    #paginator, paginated_items = loadData(request, User_ATTS_FILTER, user)
    serializer = UserReadSerializer( user ,many=True)  #paginated_items,
    return Response(serializer.data)


@api_view(['DELETE'])
#@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization('adminuser')])
def Delete_User(request, pk):
    User = get_object_or_404(User, pk=pk)
    User.delete()
    return Response(status=status.HTTP_202_ACCEPTED)