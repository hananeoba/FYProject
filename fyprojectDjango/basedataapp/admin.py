from django.contrib import admin
from .models import (
    Causes,
    Company,
    Event_Type,
    Work_Type,
    Structure,
    Installation,
    Work,
    Activity_Nature,
    Structure_Type,
)

# Register your models here.
admin.site.register(Company)
admin.site.register(Work)
admin.site.register(Work_Type)
admin.site.register(Structure)
admin.site.register(Installation)
admin.site.register(Activity_Nature)
admin.site.register(Structure_Type)
admin.site.register(Event_Type)
admin.site.register(Causes)
# end of admin.py
