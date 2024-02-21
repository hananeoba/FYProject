from django.urls import path
from . import views

urlpatterns = [
    path('Event/', views.EventListView.as_view()),
    path('Event/<str:code>/', views.EventDetailView.as_view()),
    path('EventType/', views.EventTypeListView.as_view()),
    path('EventType/<str:code>/', views.EventTypeDetailView.as_view()),
    path('Causes/', views.CausesListView.as_view()),
    path('Causes/<str:code>/', views.CausesDetailView.as_view()),
    
]
