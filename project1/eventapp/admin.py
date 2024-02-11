from django.contrib import admin
from .models import Event, EventType, Causes
# Register your models here.

admin.site.register(Event)
admin.site.register(EventType)
admin.site.register(Causes)