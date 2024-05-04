from django.urls import path, include
from .views import Event_ApiOverview, Add_Event, View_Event,View_Events ,Update_Event, Delete_Event, events_this_week, events_this_year_by_month, get_events, events_by_date_range

urlpatterns = [ 
    path("", Event_ApiOverview, name="event_api_overview"),
    path("all/", View_Events, name="all_events"),
    path("create/", Add_Event, name="create_event"),
    path("view/<int:pk>", View_Event, name="view_event"),
    path("update/<int:pk>", Update_Event, name="update_event"),
    path("item/<int:pk>/delete", Delete_Event, name="delete_event"),
    path("by-week/",events_this_week, name="events_this_week"),
    path("by-month/",events_this_year_by_month, name="events_this_year_by_month"),
    path("get_events/", get_events, name= "get_events"),
    path("by-date-range/", events_by_date_range, name="events_by_date_range"),
]
