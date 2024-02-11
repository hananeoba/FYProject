from django.urls import path
from .views import baseViewset, basedata_view

urlpatterns = [path("", basedata_view)]
