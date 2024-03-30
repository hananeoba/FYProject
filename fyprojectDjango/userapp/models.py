from django.db import models
from django.contrib.auth.models import (
    Permission,
    BaseUserManager,
    AbstractBaseUser,
)
from .utils import CustomPasswordValidator, CustomUserValidator

"""
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
"""



class CustomUserManager(BaseUserManager):
    def create_user(self, user_name, password=None, **extra_fields):
        if not user_name:
            raise ValueError("The user_name field must be set")
        # user_name = self.user
        # email = self.normalize_email(user_name)
        user = self.model(user_name=user_name, **extra_fields)
        if password:
            # Use the custom password validator
            CustomPasswordValidator(password)
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(user_name, password, **extra_fields)


class AdminGroup(AbstractBaseUser):
    code = models.CharField(max_length=50, blank=False, null=False, unique=True)
    label = models.CharField(max_length=50, blank=False, null=False, unique=True)
    permissions = models.ManyToManyField(Permission)
    class  Meta:
        db_table = 'admin_schema\".\"admingroup'

class AdminUser(AbstractBaseUser):
    user_name = models.CharField(max_length=50, blank=False,null=False, unique=True)
    email = models.EmailField(unique=True)
    last_name = models.CharField(max_length=50, blank=False)
    first_name = models.CharField(max_length=50, blank=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(
        default=False,
        help_text=(
            "Designates that this user has all permissions without "
            "explicitly assigning them."
        ),
    )
    admin_groups = models.ManyToManyField(AdminGroup, blank=True)
    is_partialy_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_password_reset = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True, null=False)
    company = models.ForeignKey(
        "basedataapp.Company", null=True, blank=True, on_delete=models.PROTECT
    )
    structure = models.ForeignKey(
        "basedataapp.Structure", null=True, blank=True, on_delete=models.PROTECT
    )
    failed_login_attempts = models.IntegerField(default=0)

    created_by = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="created_by_adminuser",
    )
    updated_by = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="updated_by_adminuser",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, null=True, editable=False, blank=True
    )
    updated_at = models.DateTimeField(null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "user_name"
    # USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.user_name

    class Meta:
        # managed = True
        db_table = 'admin_schema\".\"adminuser'
