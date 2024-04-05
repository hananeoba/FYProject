from django.urls import path
from userapp.views.group_views import (
    GroupApiOverview,
    Add_Group,
    Update_Group,
    View_Group,
    Delete_Group,
    View_Groups,
)

urlpatterns = [
    path("overview/", GroupApiOverview, name="group_api_overview"),
    path("create/", Add_Group, name="add_group"),
    path("all/", View_Groups, name="view_groups"),
    path("view/<str:pk>", View_Group, name="view_group"),
    path("update/<str:pk>", Update_Group, name="update_group"),
    path("delete/<str:pk>", Delete_Group, name="delete_group"),
]
