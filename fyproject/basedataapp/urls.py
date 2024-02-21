from django.urls import path
from . import views

urlpatterns = [
    path('company/', views.CompanyListView.as_view()),
    path('company/<str:code>/', views.CompanyDetailView.as_view()),
]
