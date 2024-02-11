from django.contrib import admin
from .models import Company, WorkType, Structure, Installation, Work, ActivityNature, StructureType

# Register your models here.
admin.site.register(Company)
admin.site.register(Work)
admin.site.register(WorkType)
admin.site.register(Structure)
admin.site.register(Installation)
admin.site.register(ActivityNature)
admin.site.register(StructureType)

#end of admin.py