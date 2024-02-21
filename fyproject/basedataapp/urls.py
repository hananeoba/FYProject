from django.urls import path
from . import views

urlpatterns = [
    # company paths
    path("company/", views.CompanyListView.as_view()),
    path("company/<str:code>/", views.CompanyDetailView.as_view()),
    # activity nature paths
    path("activitynature/", views.ActivityNatureListView.as_view()),
    path("activitynature/<str:code>/", views.ActivityNatureDetailView.as_view()),
    # structure paths
    path("structure/", views.StructureListView.as_view()),
    path("structure/<str:code>/", views.StructureDetailView.as_view()),
    # structure type paths
    path("structuretype/", views.StructureTypeListView.as_view()),
    path("structuretype/<str:code>/", views.StructureTypeDetailView.as_view()),
    # work paths
    path("work/", views.WorkListView.as_view()),
    path("work/<str:code>/", views.WorkDetailView.as_view()),
    # installation paths
    path("installation/", views.InstallationListView.as_view()),
    path("installation/<str:code>/", views.InstallationDetailView.as_view()),
    # worktype paths
    path("worktype/", views.WorkTypeListView.as_view()),
    path("worktype/<str:code>/", views.WorkTypeDetailView.as_view()),
]
