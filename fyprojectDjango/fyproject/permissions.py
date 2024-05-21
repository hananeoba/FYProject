from django.contrib.auth.models import Permission
from rest_framework import permissions


def custom_permission_generalization(model_name):
    class ModelPermission(permissions.BasePermission):
        permission_map = {
            'GET': 'view_{}',
            'POST': 'add_{}',
            'PUT': 'change_{}',
            'DELETE': 'delete_{}',
            'PATCH': 'change_{}',
        }

        def has_permission(self, request, view):
            http_method = request.method
            permission_name = self.permission_map.get(http_method).format(model_name)
            user_permissions = set()
            if request.user.is_superuser:
                return True

            if request.user.company.code.lower() == 'kernel':
                return True

            if request.user.is_staff:
                permission_check = Permission.objects.get(codename=permission_name)
                if permission_check.content_type.app_label == 'ADMIN':
                    return True
                else:
                    for group in request.user.groups.all():  # Assuming user has a 'groups' relationship
                        user_permissions.update(group.permissions.values_list('codename', flat=True))
                    return permission_name in user_permissions

            # Check if the permission_name is present in any of the user's groups' permissions

            for group in request.user.groups.all():  # Assuming user has a 'groups' relationship
                user_permissions.update(group.permissions.values_list('codename', flat=True))
            return permission_name in user_permissions

    return ModelPermission