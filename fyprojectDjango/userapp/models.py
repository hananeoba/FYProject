from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin


class AbstractUserModel(models.Model):
    created_by = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,  # this is to prevent deletion of the user
        related_name="%(class)s_created_by",  # to avoid clash of related_name
        null=True,
        blank=True,
    )
    updated_by = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,  # this is to prevent deletion of the user
        related_name="%(class)s_updated_by",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class User(AbstractUser, AbstractUserModel, PermissionsMixin):
    email = models.EmailField(
        unique=True
    )  # costomize the email field to be used instead of username
    user_company = models.ForeignKey(
        "basedataapp.Company", on_delete=models.PROTECT, null=True, blank=True
    )
    user_structure = models.ForeignKey(
        "basedataapp.Structure", on_delete=models.PROTECT, null=True, blank=True
    )
    user_role = models.CharField(max_length=100, null=True, blank=True)
    # login with email instead of username
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password", "username"]

    def __str__(self):
        return self.username
