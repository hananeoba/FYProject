from userapp.views.admin_views import (
    Logout,
    UserApiOverview,
    Add_User,
    Update_User,
    View_User,
    Delete_User,
    View_Users,
)
from django.urls import path

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
    TokenObtainPairView,
)

"""'all_items': '/all',
        'Add': '/',
        'View': '/view/pk',
        'Update': '/update/pk',
        'Delete': '/item/pk/delete'"""

urlpatterns = [
    path("overview/", UserApiOverview, name="user_api_overview"),  # /api/user/users
    path("create/", Add_User, name="add_user"),  # api/user/
    path("all/", View_Users, name="view_users"),  # api/user/all
    path("view/<str:pk>", View_User, name="view_user"),  # api/user/view/pk
    path("update/<str:pk>", Update_User, name="update_user"),  # api/user/update/pk
    path(
        "delete/<str:pk>", Delete_User, name="delete_user"
    ),  # api/user/item/pk/delete
    path(
        "login/", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),  # api/user/login
    path(
        "token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),  # api/user/token/refresh
    path(
        "token/verify/", TokenVerifyView.as_view(), name="token_verify"
    ),  # api/user/token/verify
    path("logout/", Logout, name="logout"),  # api/user/logout

]