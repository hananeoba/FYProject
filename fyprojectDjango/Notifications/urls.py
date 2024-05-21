from django.urls import path

from .views import get_Notification, get_New_Notification, set_Notification_Read

urlpatterns = [ 
    path('get_notifications/', get_Notification, name='get_notifications'),
    path('get_new_notification/', get_New_Notification, name='get_new_notification'),
    path('set_notification_read/', set_Notification_Read, name='set_notification_read'),
]