from django.urls import path, include
from .views import Event_ApiOverview, Add_Event, View_Event,View_Events ,Update_Event, Delete_Event

urlpatterns = [ 
    path("", Event_ApiOverview, name="event_api_overview"),
    path("all", View_Events, name="all_events"),
    path("create", Add_Event, name="create_event"),
    path("view/<int:pk>", View_Event, name="view_event"),
    path("update/<int:pk>", Update_Event, name="update_event"),
    path("item/<int:pk>/delete", Delete_Event, name="delete_event"),
   
]
