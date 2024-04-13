from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from basedataapp.models import Province, State
from basedataapp.serializer import Province_Serializer, Province_Read_Serializer

from basedataapp.utils import generate_new_code
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
        'Delete': '/delete/pk'
    }

    return Response(api_urls)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization('province')])
def Add_Province(request):
    data= request.data  # Create a mutable copy of the QueryDict
    state_json = data.get('state')
    state_id = state_json.get('id')
    # Validating for already existing data
    if State.objects.filter(id=state_id).exists():
        data['state'] = state_id 
    else :
        raise serializers.ValidationError('State does not exist')
    # Checking if Province with the given data already exists
    code = generate_new_code(data.get('code'))
    if Province.objects.filter(code=code).exists():
        raise serializers.ValidationError('This data already exists')

    province_serializer = Province_Serializer(data=data, context={"request": request})

    if province_serializer.is_valid():
        province_serializer.save()
        return Response(province_serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(province_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization('province')])
def Update_Province(request, pk):
    province = Province.objects.get(pk=pk)
    data= request.data  # Create a mutable copy of the QueryDict
    state_json = data.get('state')
    state_id = state_json.get('id')
    # Validating for already existing data
    if State.objects.filter(id=state_id).exists():
        data['state'] = state_id 
    else :
        raise serializers.ValidationError('State does not exist')

    serializer = Province_Serializer(instance=province, data=data, context={'request': request})

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, data= serializer.errors)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization('province')])
def View_Province(request, pk):
    province = Province.objects.get(pk=pk)
    if province:
        serializer = Province_Read_Serializer(province, context={"request": request})
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization('province')])
def View_Provinces(request):
    current_user = request.user
    state_id = request.query_params.get("state_id",None)

    if state_id:
        data = Province.objects.filter(state=state_id)
    else:   
        #if is_kernel(current_user):
        data = Province.objects.all()
        #else:
           # data = Company.objects.filter(id=current_user.company.id)
    serializer = Province_Read_Serializer( data , many=True, context= {"request": request})#data
    return Response(serializer.data)


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization('province')])
def Delete_Province(request, pk):
    province = get_object_or_404(Province, pk=pk)
    province.delete()
    return Response(status=status.HTTP_202_ACCEPTED, data='Item deleted')

"""------------------------------------------------------------------------------------------------"""
