from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Company

from .serializer import CompanySerializer

# Create your views here.
@api_view(['GET', 'POST'])
def company_view(request, pk= None, *args, **kwargs):
    method = request.method
    if method == 'GET': 
        #detail view
        if pk is not None:
            """
            "this is the other way to do it using filter"
            queryset = Company.objects.filter(pk=pk)
            if not queryset.exists():
                return Response({}, status = 404)
            data = CompanySerializer(queryset).data
            return Response(data)
            """
            company = get_object_or_404(Company, pk=pk)
            data = CompanySerializer(company).data
            return Response(data)
        else :
        #list view 
            queryset = Company.objects.all()
            data = CompanySerializer(queryset, many=True).data
            return Response(data)
    if method == 'POST':
         #creatte company
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"invalid": "not good data"}, status = 400)
    