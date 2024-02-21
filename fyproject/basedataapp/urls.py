from django.urls import path
from . import views

urlpatterns = [
    path('company/', views.CompanyView.as_view()),
    path('company/<int:pk>/', views.CompanyDetail.as_view()),
    path('company/<int:pk>/update/', views.CompanyUpdate.as_view()),
    path('company/<int:pk>/delete/', views.CompanyDelete.as_view()),
]
