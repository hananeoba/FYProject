from rest_framework import permissions

from .permissions import (
    CanModifyOrViewPermissionDataBase,
    CanModifyOrViewPermissionEvent,
    CanModifyOrViewPermissionUser,
)


class BaseEditorPermissionMixin:
    permission_classes = [CanModifyOrViewPermissionDataBase]


class EventEditorPermissionMixin:
    permission_classes = [CanModifyOrViewPermissionEvent]


class UserEditorPermissionMixin:
    permission_classes = [CanModifyOrViewPermissionUser]
