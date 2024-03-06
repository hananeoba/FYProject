from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from basedataapp.models import Province, State
from basedataapp.serializer import Province_Serializer, Province_Read_Serializer

from fyproject.permissions import custom_permission_generalization
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import serializers

"""-------------------------------------------PROVINCE------------------------------------------------"""


# Province Views
@api_view(['GET'])
def Province_ApiOverview(request):
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
@permission_classes([IsAuthenticated, custom_permission_generalization('province')])
def Add_Province(request):
    data = request.data
    state_json = data.get('state')
    state_id = state_json.get('id')

    # Validating for already existing data
    if State.objects.filter(id=state_id).exists():
        data['state'] = state_id

        # Checking if Province with the given data already exists
        if Province.objects.filter(**data).exists():
            raise serializers.ValidationError('This data already exists')

        province_serializer = Province_Serializer(data=data)

        if province_serializer.is_valid():
            province_serializer.save()
            return Response(province_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(province_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization('province')])
def Update_Province(request, pk):
    province = Province.objects.get(pk=pk)
    data = Province_Serializer(instance=province, data=request.data, context={'request': request})

    if data.is_valid():
        data.save()
        return Response(data.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization('province')])
def View_Province(request, pk):
    province = Province.objects.get(pk=pk)
    if province:
        serializer = Province_Read_Serializer(province)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization('province')])
def View_Provinces(request):
    #paginator, data = , PROVINCE_ATTS_FILTER, Province)
    objects = Province.objects.all()
    serializer = Province_Read_Serializer(  objects , many=True)#data
    return Response(serializer.data)


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization('province')])
def Delete_Province(request, pk):
    province = get_object_or_404(Province, pk=pk)
    province.delete()
    return Response(status=status.HTTP_202_ACCEPTED)

"""------------------------------------------------------------------------------------------------"""
