from django.shortcuts import get_object_or_404
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from basedataapp.models import Structure
from basedataapp.serializer import Structure_Serializer, Structure_Read_Serializer

from fyproject.permissions import custom_permission_generalization
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import serializers

"""-------------------------------------------STRUCTURE------------------------------------------------"""

@api_view(['GET'])
def Structure_ApiOverview(request):
    api_urls = {
        'all_items': '/all',
        'Add': '/create',
        'View': '/view/pk',
        'Update': '/update/pk',
        'Delete': '/item/pk/delete'
    }

    return Response(api_urls)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization('structure')])
def Add_Structure(request):
    structure = Structure_Serializer(data=request.data, context={'request': request})

    # validating for already existing data
    if Structure.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')

    if structure.is_valid():
        structure.save()
        return Response(structure.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization('structure')])
def Update_Structure(request, pk):
    structure = Structure.objects.get(pk=pk)
    data = Structure_Serializer(instance=structure, data=request.data, context={'request': request})

    if data.is_valid():
        data.save()
        return Response(data.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization('structure')])
def View_Structure(request, pk):
    structure = Structure.objects.get(pk=pk)
    if structure:
        serializer = Structure_Read_Serializer(structure)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization('structure')])
def View_Structures(request):
    data = Structure.objects.all()
    serializer = Structure_Serializer(data, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization('structure')])
def Delete_Structure(request, pk):
    structure = get_object_or_404(Structure, pk=pk)
    structure.delete()
    return Response(status=status.HTTP_202_ACCEPTED)


"""-----------------------------------------------------------------------------------------------------"""
