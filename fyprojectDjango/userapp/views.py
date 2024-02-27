from .models import User
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
