from django.shortcuts import get_object_or_404

from rest_framework import generics, mixins
from .models import (Company, WorkType, Structure, Installation, Work, ActivityNature, StructureType)

from .serializer import (CompanySerializer, AcivityNatureSerializer, WorkTypeSerialiser, StructureSerializer, InstallationSerializer, WorkSerializer, StructureTypeSerializer)  
  

# Create your views here.
class CompanyView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class CompanyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer