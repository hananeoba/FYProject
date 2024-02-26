from rest_framework.routers import DefaultRouter
from .views import EventViewSet, EventTypeViewSet, CausesViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')
router.register(r'event-types', EventTypeViewSet, basename='eventtype')
router.register(r'causes', CausesViewSet, basename='causes')
