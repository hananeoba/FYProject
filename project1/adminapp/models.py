from django.db import models
from basedata.models import AbstrctBaseModel, Company, Structure

# Create your models here.


class Permission(models.Model):
    permission_id = models.AutoField(primary_key=True)
    permission_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.permission_name


class Group(models.Model):
    group_id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=100, unique=True)
    group_permission = models.ManyToManyField(Permission, on_delete=models.PROTECT)

    def __str__(self):
        return self.group_name


class User(AbstrctBaseModel):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=100, unique=True)
    user_email = models.EmailField(max_length=100, unique=True)
    user_password = models.CharField(max_length=100)
    user_company = models.ForeignKey(Company, on_delete=models.PROTECT)
    user_structure = models.ForeignKey(Structure, on_delete=models.PROTECT)
    user_group = models.ManyToManyField(Group, on_delete=models.PROTECT)
    user_role = models.CharField(max_length=100)

    def __str__(self):
        return self.user_name
