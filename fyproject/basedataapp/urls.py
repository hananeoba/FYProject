from django.urls import path
from . import views

urlpatterns = [
    path('company/', views.company_view),
    path('company/<int:pk>', views.company_view),
]
