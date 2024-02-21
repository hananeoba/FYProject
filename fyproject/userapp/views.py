from django.shortcuts import render
from rest_framework import generics, authentication, permissions
from django.contrib.auth.hashers import make_password

from .models import User
from .serializer import UserSerializer
from django.utils import timezone

class CreatedFieldsMixin:
    def perform_create(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()
        created_fields = {
            'created_by': self.request.user if self.request.user.is_authenticated else None,
            'updated_by': None,
            'created_at': timezone.now(),
            'updated_at': None,
            'password': make_password(serializer.validated_data['password'])
        }
        serializer.save(**created_fields)
        
    def perform_update(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()
        updated_fields = {
            
            'updated_by': self.request.user if self.request.user.is_authenticated else None,
            'updated_at': timezone.now(),
            'password': make_password(serializer.validated_data['password'])
        }
        serializer.save(**updated_fields)

 # Import the missing module

class UserListView(CreatedFieldsMixin, generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    """authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    """
class UserDetailView(CreatedFieldsMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
# Create your views here.
