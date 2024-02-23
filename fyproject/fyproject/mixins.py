from rest_framework import permissions


class CompanyEditorPermissionMixin:
    permission_classes = [permissions.AllowAny ]