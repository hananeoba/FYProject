from rest_framework.routers import DefaultRouter
from .views import (
    CompanyViewSet,
    StructureViewSet,
    ActivityNatureViewSet,
    StructureTypeViewSet,
    WorkViewSet,
    WorkTypeViewSet,
    InstallationViewSet,
)

# Create a router and register your viewsets with it.
router = DefaultRouter()
router.register(r'companies', CompanyViewSet, basename='code')
router.register(r'structures', StructureViewSet, basename='structure')
router.register(r'activity-natures', ActivityNatureViewSet, basename='activitynature')
router.register(r'structure-types', StructureTypeViewSet, basename='structuretype')
router.register(r'works', WorkViewSet, basename='work')
router.register(r'work-types', WorkTypeViewSet, basename='worktype')
router.register(r'installations', InstallationViewSet, basename='installation')
