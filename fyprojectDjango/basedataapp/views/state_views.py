from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from basedataapp.models import State
from basedataapp.serializer import State_Serializer

from fyproject.permissions import custom_permission_generalization
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import serializers


"""-------------------------------------------STATE------------------------------------------------"""


@api_view(["GET"])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated, custom_permission_generalization('state')])
def State_ApiOverview(request):
    api_urls = {
        "all_items": "/all",
        "Add": "/create",
        "View": "/view/pk",
        "Update": "/update/pk",
        "Delete": "/item/pk/delete",
    }

    return Response(api_urls)


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization("state")])
def Add_State(request):
    state = State_Serializer(data=request.data, context={"request": request})

    # validating for already existing data
    if State.objects.filter(**request.data).exists():
        raise serializers.ValidationError("This data already exists")

    if state.is_valid():
        state.save()
        return Response(state.data, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["PUT"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization("state")])
def Update_State(request, pk):
    state = State.objects.get(pk=pk)
    data = State_Serializer(
        instance=state, data=request.data, context={"request": request}
    )

    if data.is_valid():
        data.save()
        return Response(data.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization("state")])
def View_State(request, pk):
    state = State.objects.get(pk=pk)
    if state:
        serializer = State_Serializer(state)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization("state")])
def View_States(request):
    #data = , STATE_ATTS_FILTER, State)
    states = State.objects.all()
    serializer = State_Serializer(states, many=True)
    return Response(serializer.data)


@api_view(["DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization("state")])
def Delete_State(request, pk):
    state = get_object_or_404(State, pk=pk)
    state.delete()
    return Response(status=status.HTTP_202_ACCEPTED)


"""------------------------------------------------------------------------------------------------"""

