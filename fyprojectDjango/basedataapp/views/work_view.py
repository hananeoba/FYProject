from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from basedataapp.models import Work
from basedataapp.serializer import Work_Serializer, Work_Read_Serializer

from fyproject.permissions import custom_permission_generalization
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import serializers


"""-------------------------------------------WORK------------------------------------------------"""

@api_view(['GET'])
def Work_ApiOverview(request):
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
@permission_classes([IsAuthenticated, custom_permission_generalization('work')])
def Add_Work(request):
    work = Work_Serializer(data=request.data, context={'request': request})

    # validating for already existing data
    if Work.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')

    if work.is_valid():
        work.save()
        return Response(work.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization('work')])
def Update_Work(request, pk):
    work = Work.objects.get(pk=pk)
    data = Work_Serializer(instance=work, data=request.data, context={'request': request})

    if data.is_valid():
        data.save()
        return Response(data.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization('work')])
def View_Work(request, pk):
    work = Work.objects.get(pk=pk)
    if work:
        serializer = Work_Read_Serializer(work)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization('work')])
def View_Works(request):
    data = Work.objects.all()
    serializer = Work_Read_Serializer(data, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization('work')])
def Delete_Work(request, pk):
    work = get_object_or_404(Work, pk=pk)
    work.delete()
    return Response(status=status.HTTP_202_ACCEPTED)
"""--------------------------------------------------------------------------------------------------"""
