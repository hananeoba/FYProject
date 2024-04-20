from django.shortcuts import get_object_or_404
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from basedataapp.models import Causes, Work, Event_Type
from basedataapp.utils import generate_new_code

from django.db.models import Count
from django.db.models.functions import TruncWeek, TruncMonth, TruncDay, TruncYear
from datetime import datetime, timedelta

from .models import Event
from .serializer import Event_Serializer, Event_Read_Serializer
from fyproject.permissions import custom_permission_generalization
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import serializers


"""-------------------------------------------EVENT------------------------------------------------"""


@api_view(["GET"])
def Event_ApiOverview(request):
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
@permission_classes([IsAuthenticated, custom_permission_generalization("event")])
def Add_Event(request):
    data = request.data
    work_json = data.get("work")
    event_type = data.get("event_type")
    causes_json = data.get("event_causes")
    # Validating for already existing data
    if work_json:
        work_id = work_json.get("id")
        if Work.objects.filter(id=work_id).exists():
            data["work"] = work_id
        else:
            raise serializers.ValidationError("This work does not exist")
    else:
        work_id = None
    if event_type:
        event_type_id = event_type.get("id")
        if Event_Type.objects.filter(id=event_type_id).exists():
            data["event_type"] = event_type_id
        else:
            raise serializers.ValidationError("This event type does not exist")
    else:
        event_type_id = None
    if causes_json:
        causes_id = [cause.get("id") for cause in causes_json]
        if Causes.objects.filter(id__in=causes_id).exists():
            data["event_causes"] = causes_id
        else:
            raise serializers.ValidationError("This cause does not exist")

    # Checking if data is valid and exists
    # Checking if event with the given data already exists
    code = generate_new_code(data.get("code"))
    if Event.objects.filter(code=code).exists():
        raise serializers.ValidationError("This data already exists")
    serializer = Event_Serializer(data=data, context={"request": request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization("event")])
def Update_Event(request, pk):
    event = event.objects.get(pk=pk)
    data = Event_Serializer(
        instance=event, data=request.data, context={"request": request}
    )

    if data.is_valid():
        data.save()
        return Response(data.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization("event")])
def View_Event(request, pk):
    event = Event.objects.get(pk=pk)
    if event:
        serializer = Event_Read_Serializer(event)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization("event")])
def View_Events(request):
    selectedInstallation_json = request.query_params.get("selectedInstallation")
    if selectedInstallation_json:
        selected_installation_id = selectedInstallation_json.get("id")
        work = Work.objects.filter(installation=selected_installation_id)
        data = Event.objects.filter(work=work)
    else:
        data = Event.objects.all()
    serializer = Event_Read_Serializer(data, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization("event")])
def events_this_week(request):
    # Define the start and end dates for the current week
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday()) - timedelta(days=1)
    end_of_week = start_of_week + timedelta(days=6)

    # Generate a list of dates for the current week
    dates_this_week = [start_of_week + timedelta(days=i) for i in range(7)]

    # Query to get the count of events for each day within the time range
    events_this_week = (
        Event.objects.filter(start_date__date__range=[start_of_week, end_of_week])
        .annotate(day=TruncDay("start_date"))
        .values("day")
        .annotate(count=Count("id"))
    )

    # Create a dictionary to hold the counts for each day
    events_per_day = {item["day"].date(): item["count"] for item in events_this_week}

    # Fill in missing days with a count of 0
    for date in dates_this_week:
        if date not in events_per_day:
            events_per_day[date] = 0

    # Sort the dictionary by date
    sorted_events_per_day = dict(sorted(events_per_day.items()))

    # Prepare the response data
    response_data = [
        {"day": date.strftime("%Y-%m-%d"), "count": count}
        for date, count in sorted_events_per_day.items()
    ]

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization("event")])
def events_this_year_by_month(request):
    # Define the start and end dates for the current year
    today = datetime.now().date()
    start_of_year = today.replace(month=1, day=1)
    end_of_year = today.replace(month=12, day=31)

    # Generate a list of months for the current year
    months_this_year = [start_of_year.replace(month=i) for i in range(1, 13)]

    # Query to get the count of events for each month within the current year
    events_this_year = (
        Event.objects.filter(start_date__date__range=[start_of_year, end_of_year])
        .annotate(month=TruncMonth("start_date"))
        .values("month")
        .annotate(count=Count("id"))
    )

    # Create a dictionary to hold the counts for each month
    events_per_month = {
        item["month"].date(): item["count"] for item in events_this_year
    }

    # Fill in missing months with a count of 0
    for month in months_this_year:
        if month not in events_per_month:
            events_per_month[month] = 0

    # Sort the dictionary by month
    sorted_events_per_month = dict(sorted(events_per_month.items()))

    # Prepare the response data
    response_data = [
        {"month": month.strftime("%m-%y"), "count": count}
        for month, count in sorted_events_per_month.items()
    ]

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(["DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization("event")])
def Delete_Event(request, pk):
    event = get_object_or_404(event, pk=pk)
    event.delete()
    return Response(status=status.HTTP_202_ACCEPTED)


"""--------------------------------------------------------------------------------------------------"""
