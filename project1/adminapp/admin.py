from django.contrib import admin
from .models import Permission, Group, User

# Register your models here.
admin.site.register(Permission)
admin.site.register(Group)
admin.site.register(User)
