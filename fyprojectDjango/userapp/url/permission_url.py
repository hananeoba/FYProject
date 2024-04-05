from django.urls import path
from userapp.views.permission_views import (
    PermissionOverview,
    View_Permission,
    View_Permissions,
)

urlpatterns = [
    path("overview/", PermissionOverview, name="permission_api_overview"),
    path("all/", View_Permissions, name="view_permissions"),
    path("view/<str:pk>", View_Permission, name="view_permission"),
]
