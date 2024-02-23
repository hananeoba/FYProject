from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import User
from .serializer import UserSerializer
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from fyproject.mixins import CompanyEditorPermissionMixin

class UserViewSet(
    CompanyEditorPermissionMixin,
    viewsets.ModelViewSet,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['list', 'create']:
            return [permissions.IsAuthenticated()]
        else:
            return [CompanyEditorPermissionMixin()]  # Adjust as needed

    def perform_create(self, serializer):
        created_fields = {
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
