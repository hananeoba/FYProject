from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):
    user_company = models.ForeignKey('basedataapp.Company', on_delete=models.PROTECT, null=True, blank=True)
    user_structure = models.ForeignKey('basedataapp.Structure', on_delete=models.PROTECT, null=True, blank=True)
    user_group = models.ForeignKey(Group, on_delete=models.PROTECT, null=True, blank=True, related_name='%(class)s_user_group')
    user_permissions = models.ForeignKey(Permission, on_delete=models.PROTECT, null=True, blank=True, related_name='%(class)s_user_permissions')
    user_role = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.username
