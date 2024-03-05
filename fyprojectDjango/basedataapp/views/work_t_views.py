from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from basedataapp.models import  Work_Type
from basedataapp.serializer import Work_Type_Read_Serializer, Work_Type_Serializer

from fyproject.permissions import custom_permission_generalization
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import serializers


"""-------------------------------------------WORK_TYPE------------------------------------------------"""

@api_view(['GET'])
def Work_Type_ApiOverview(request):
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
@permission_classes([IsAuthenticated, custom_permission_generalization('work_type')])
def Add_Work_Type(request):
    work_type = Work_Type_Serializer(data=request.data, context={'request': request})

    # validating for already existing data
    if Work_Type.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')

    if work_type.is_valid():
        work_type.save()
        return Response(work_type.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization('work_type')])
def Update_Work_Type(request, pk):
    work_type = Work_Type.objects.get(pk=pk)
    data = Work_Type_Serializer(instance=work_type, data=request.data, context={'request': request})

    if data.is_valid():
        data.save()
        return Response(data.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization('work_type')])
def View_Work_Type(request, pk):
    work_type = Work_Type.objects.get(pk=pk)
    if work_type:
        serializer = Work_Type_Read_Serializer(work_type)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization('work_type')])
def View_Work_Types(request):
    data = Work_Type.objects.get.all()
    serializer = Work_Type_Read_Serializer(data, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization('work_type')])
def Delete_Work_Type(request, pk):
    work_type = get_object_or_404(Work_Type, pk=pk)
    work_type.delete()
    return Response(status=status.HTTP_202_ACCEPTED)

"""------------------------------------------------------------------------------------------------"""
