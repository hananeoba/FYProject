from .views import MyTokenObtainPairView
from .routers import router

from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path("", include(router.urls)),#/api/user/users
    path("login/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),#api/user/login
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),#api/user/token/refresh
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),#api/user/token/verify
]
# other paths...
