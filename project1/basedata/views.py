from rest_framework import generics
from rest_framework import viewsets
# from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status

from . import models
from . import serializers

from .models import Company


class baseViewset(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = serializers.CompanySerializer
    
basedata_view=baseViewset.as_view() 