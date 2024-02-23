
from .routers import  router
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path, include


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', obtain_auth_token),

]
    # other paths...
