from django.shortcuts import get_object_or_404
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from basedataapp.models import Causes, Structure, Work, Event_Type
from basedataapp.utils import (
    generate_Event_code,
    get_children_structures,
    get_parent_structures,
)

from django.db.models import Count
from django.db.models import Q
from django.db.models.functions import TruncWeek, TruncMonth, TruncDay, TruncYear
from datetime import datetime, timedelta

from userapp.utils import is_kernel

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
    user = request.user
    structure = user.structure
    company = user.company
    year = data.get("start_date")[:4]
    count = Event.objects.all().count() + 1
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
    code = generate_Event_code(year=year, company=company, struc=structure, count=count)
    label = code
    if Event.objects.filter(code=code).exists():
        raise serializers.ValidationError("This data already exists")
    data["code"] = code
    data["label"] = label

    serializer = Event_Serializer(data=data, context={"request": request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(
            {"Error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["PUT"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, custom_permission_generalization("event")])
def Update_Event(request, pk):
    event = Event.objects.get(pk=pk)
    data = request.data
    data["code"] = event.code
    data["label"] = event.label

    data = Event_Serializer(instance=event, data=data, context={"request": request})

    if data.is_valid():
        data.save()
        return Response(data.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, data=data.errors)


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
    user = request.user
    selectedInstallation_json = request.query_params.get("installation_id")
    if selectedInstallation_json:
        selected_installation_id = selectedInstallation_json.get("id")
        work = Work.objects.filter(installation=selected_installation_id)
        data = Event.objects.filter(work=work)
    else:
        if is_kernel(user):
            data = Event.objects.all()
        else:
            data = Event.objects.filter(work__installation__structure=user.structure)
        # data = Event.objects.all();
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
    structures = get_children_structures(request.user.structure.id)
    # Generate a list of months for the current year
    months_this_year = [start_of_year.replace(month=i) for i in range(1, 13)]

    # Query to get the count of events for each month within the current year
    events_this_year = (  # work__installation__structure__in=structures
        Event.objects.filter(
            Q(
                start_date__date__range=[start_of_year, end_of_year],
                work__installation__structure__in=structures,
            )
            | Q(created_by=request.user.id)
        )
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


from datetime import datetime, timedelta
from django.db.models import Count
from django.db.models.functions import TruncDay
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication

# Define your custom_permission_generalization function or import it if defined elsewhere
# from your_app.permissions import custom_permission_generalization


@api_view(["GET"])
@permission_classes([IsAuthenticated, custom_permission_generalization("event")])
@authentication_classes([JWTAuthentication])
def events_by_date_range(request):
    try:
        # Get start and end date parameters from query string
        start_date_str = request.query_params.get("start_date")
        end_date_str = request.query_params.get("end_date")
        structure_ids = request.query_params.getlist("structure_ids")

        # Parse start and end dates from query parameters
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            return Response(
                {
                    "error": "Invalid date format. Please provide dates in YYYY-MM-DD format."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Ensure end_date is not before start_date
        if end_date < start_date:
            return Response(
                {"error": "End date must be on or after start date."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Filter events by the date range and the provided structure IDs
        if structure_ids:
            date_range = [
                start_date + timedelta(days=i)
                for i in range((end_date - start_date).days + 1)
            ]
            data = []
            for structure_id in structure_ids:
                events = (
                    Event.objects.filter(
                        start_date__date__range=[start_date, end_date],
                        work__installation__structure=structure_id,
                    )
                    .annotate(day=TruncDay("start_date"))
                    .values("day")
                    .annotate(count=Count("id"))
                )

                # Create a dictionary to map each date to its count
                event_dict = {
                    event["day"].strftime("%Y-%m-%d"): event["count"]
                    for event in events
                }

                # Initialize data_events with zero counts for all dates in the range
                data_events = [{"day": day, "count": 0} for day in date_range]
                # Update data_events with actual counts from events
                for event in data_events:
                    if event["day"].strftime("%Y-%m-%d") in event_dict:
                        event["count"] = event_dict[event["day"].strftime("%Y-%m-%d")]
                data.append(
                    {
                        "structure_code": Structure.objects.get(id=structure_id).code,
                        "events": data_events,
                    }
                )
            return Response(data, status=status.HTTP_200_OK)
        else:

            user_id = request.user.id
            events_by_date_range = (
                Event.objects.filter(
                    start_date__date__range=[start_date, end_date],
                    created_by=user_id,
                )
                .annotate(day=TruncDay("start_date"))
                .values("day", "work__installation__structure")
                .annotate(count=Count("id"))
            )

            # Generate a list of all days in the date range
            days_of_range = [
                start_date + timedelta(days=i)
                for i in range((end_date - start_date).days + 1)
            ]
            # Fetch structure names
            structure = Structure.objects.get(id=structure_id)
            response = [
                {
                    "structure_code": structure.code,
                    "events": [
                        {"day": event["day"], "count": event["count"]}
                        for event in events_by_date_range
                    ],
                }
            ]
            # Create a dictionary to hold the counts for each day and structure
            # Prepare the response data
            return Response(response, status=status.HTTP_200_OK)
    except Exception as e:
        print(repr(e))
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST,
        )
    # Generate a list of all days in the date range


"""--------------------------------------------------------------------------------"""


@api_view(["GET"])
def get_events(request):
    user = request.user
    if is_kernel(user):
        events = Event.objects.all()
        serializer = Event_Read_Serializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif user.structure is None:
        events = (
            Event.objects.none()
        )  # Return an empty queryset if user has no structure
        serializer = Event_Read_Serializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Initialize a list to store events from all parent structures
    events = []

    # Start from the current user's structure
    current_structure = user.structure.id

    # Traverse the hierarchy until there's no parent structure left
    structures = get_children_structures(current_structure)
    events = Event.objects.filter(
        Q(work__installation__structure__in=structures) | Q(created_by=request.user.id)
    ).order_by("structure")
    serializer = Event_Read_Serializer(events, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


"""
current_user = event.created_by
users_list = []
current_Structure = get_parent_structure(current_user.structure)
id_struct=[struct.get(id) for struct in current_structure]
users_list= User.objects.filter(structure__in=id_struct)
notification.users = [user.id for user in users_list]
notification.event = event
notification.save()
signal(notificqtion)

users_mail = [user.email for user in users_list]
email from to list object=$ message un incindent est apprru dans structere ouvrqge dqte event type
"""
