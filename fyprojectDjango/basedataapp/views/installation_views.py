from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from basedataapp.models import Installation, Structure
from basedataapp.serializer import Installation_Serializer

from fyproject.permissions import custom_permission_generalization
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import serializers

"""-------------------------------------------INSTALATION------------------------------------------------"""

@api_view(['GET'])
def Installation_ApiOverview(request):
    api_urls = {
        'all_items': '/all',
        'Add': '/create',
        'View': '/view/pk',
        'Update': '/update/pk',
        'Delete': '/delete/pk'
    }

    return Response(api_urls)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization('installation')])
def Add_Installation(request):
    data = request.data
    structure_json = data.get('structure')
    structure_id = structure_json.get('id')

    # Validating for already existing data
    if Structure.objects.filter(id=structure_id).exists():
        data['structure'] = structure_id

        # Checking if Installation with the given data already exists
        if Installation.objects.filter(**data).exists():
            raise serializers.ValidationError('This data already exists')

        installation_serializer = Installation_Serializer(data=data, context={'request': request})

        if installation_serializer.is_valid():
            installation_serializer.save()
            return Response(installation_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(installation_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization('installation')])
def Update_Installation(request, pk):
    installation = Installation.objects.get(pk=pk)
    data = Installation_Serializer(instance=installation, data=request.data, context={'request': request})

    if data.is_valid():
        data.save()
        return Response(data.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization('installation')])
def View_Installation(request, pk):
    installation = Installation.objects.get(pk=pk)
    if installation:
        serializer = Installation_Serializer(installation)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization('installation')])
def View_Installations(request):
    data = Installation.objects.all()
    serializer = Installation_Serializer(data, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization('installation')])
def Delete_Installation(request, pk):
    installation = get_object_or_404(Installation, pk=pk)
    installation.delete()
    return Response(status=status.HTTP_202_ACCEPTED)
"""-------------------------------------------------------------------------------------------------"""
