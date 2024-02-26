from django.urls import path, include
from .routers import router
# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
