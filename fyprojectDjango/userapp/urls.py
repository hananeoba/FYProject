from django.urls import path, include
import userapp
urlpatterns = [
    path("user/", include("userapp.url.user_url")),
    path("group/", include("userapp.url.group_url")),
    path("permission/", include("userapp.url.permission_url")),
    
]