from rest_framework import status
from fyproject.permissions import custom_permission_generalization
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Notification, Notification_User
from .serializers import NotificationSerializer
from userapp.models import AdminUser

"""-------------------------------------------NOTIFICATION------------------------------------------------"""


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
def get_Notification(request):
    notification = Notification.objects.filter(users=request.user.id).order_by("-date")
    notification_ser = NotificationSerializer(notification, many=True)
    return Response(notification_ser.data)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
def get_New_Notification(request):
    notification = Notification.objects.filter(users=request.user.id).latest("id")
    notification_ser = NotificationSerializer(notification)
    return Response(notification_ser.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def set_Notification_Read(request):
    try:
        # Retrieve the specific Notification_User instance
        notification = Notification_User.objects.get(
            user_id=request.user.id, notification_id=request.data["notification_id"]
        )
        return Response(
            status=status.HTTP_200_OK, data={"message": "Notification marked as read"}
        )
    except Notification_User.DoesNotExist:
        return Response(
            status=status.HTTP_404_NOT_FOUND, data={"message": "Notification not found"}
        )
