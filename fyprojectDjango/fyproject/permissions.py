from rest_framework import permissions


class CanModifyOrViewPermissionDataBase(permissions.BasePermission):
# basebataapp permissions 
    def has_permission(self, request, view):

        if view.__class__.__name__ == "CompanyViewSet":
            if request.method == "GET":
                return request.user.has_perm("basedataapp.view_company")

            if (
                request.method == "POST"# create 
                or request.method == "DELETE"# or delete
                or request.method == "PUT"  # or update
                or request.method == "PATCH"
            ):
                return (
                    request.user.has_perm("basedataapp.delete_company")
                    or request.user.has_perm("basedataapp.add_company")
                    or request.user.has_perm("basedataapp.change_company")
                )
        if view.__class__.__name__ == "StructureViewSet":
            if request.method == "GET":
                return request.user.has_perm("basedataapp.view_structure")

            if (
                request.method == "POST"
                or request.method == "DELETE"
                or request.method == "PUT"
                or request.method == "PATCH"
            ):
                return (
                    request.user.has_perm("basedataapp.delete_Structure")
                    or request.user.has_perm("basedataapp.add_Structure")
                    or request.user.has_perm("basedataapp.change_Structure")
                )
        if view.__class__.__name__ == "ActivityNatureViewSet":
            if request.method == "GET":
                return request.user.has_perm("basedataapp.view_activitynature")

            if (
                request.method == "POST"
                or request.method == "DELETE"
                or request.method == "PUT"
                or request.method == "PATCH"
            ):
                return (
                    request.user.has_perm("basedataapp.delete_activitynature")
                    or request.user.has_perm("basedataapp.add_activitynature")
                    or request.user.has_perm("basedataapp.change_activitynature")
                )
        if view.__class__.__name__ == "WorkTypeViewSet":
            if request.method == "GET":
                return request.user.has_perm("basedataapp.view_worktype")

            if (
                request.method == "POST"
                or request.method == "DELETE"
                or request.method == "PUT"
                or request.method == "PATCH"
            ):
                return (
                    request.user.has_perm("basedataapp.delete_worktype")
                    or request.user.has_perm("basedataapp.add_worktype")
                    or request.user.has_perm("basedataapp.change_worktype")
                )
        if view.__class__.__name__ == "WorkViewSet":
            if request.method == "GET":
                return request.user.has_perm("basedataapp.view_work")

            if (
                request.method == "POST"
                or request.method == "DELETE"
                or request.method == "PUT"
                or request.method == "PATCH"
            ):
                return (
                    request.method == "POST"
                    or request.method == "DELETE"
                    or request.method == "PUT"
                    or request.method == "PATCH"
                ) and (
                    request.user.has_perm("basedataapp.delete_work")
                    or request.user.has_perm("basedataapp.add_work")
                    or request.user.has_perm("basedataapp.change_work")
                )
        if view.__class__.__name__ == "StructureTypeViewSet":
            if request.method == "GET":
                return request.user.has_perm("basedataapp.view_structuretype")

            if (
                request.method == "POST"
                or request.method == "DELETE"
                or request.method == "PUT"
                or request.method == "PATCH"
            ):
                return (
                    request.user.has_perm("basedataapp.delete_structuretype")
                    or request.user.has_perm("basedataapp.add_structuretype")
                    or request.user.has_perm("basedataapp.change_structuretype")
                )
        if view.__class__.__name__ == "InstallationViewSet":
            if request.method == "GET":
                return request.user.has_perm("basedataapp.view_installation")

            if (
                request.method == "POST"
                or request.method == "DELETE"
                or request.method == "PUT"
                or request.method == "PATCH"
            ):
                return (
                    request.user.has_perm("basedataapp.delete_installation")
                    or request.user.has_perm("basedataapp.add_installation")
                    or request.user.has_perm("basedataapp.change_installation")
                )
        return False
        # Check if the user has the necessary permissions to delete or update or create


class CanModifyOrViewPermissionEvent(permissions.BasePermission):
    # eventapp permissions 
    def has_permission(self, request, view):
        if view.__class__.__name__ == "EventViewSet":
            if request.method == "GET":
                return request.user.has_perm("eventapp.view_event")

            if (
                request.method == "POST"
                or request.method == "DELETE"
                or request.method == "PUT"
                or request.method == "PATCH"
            ):
                return (
                    request.user.has_perm("eventapp.delete_event")
                    or request.user.has_perm("eventapp.add_event")
                    or request.user.has_perm("eventapp.change_event")
                )
        if view.__class__.__name__ == "EventTypeViewSet":
            if request.method == "GET":
                return request.user.has_perm("eventapp.view_eventtype")

            if (
                request.method == "POST"
                or request.method == "DELETE"
                or request.method == "PUT"
                or request.method == "PATCH"
            ):
                return (
                    request.user.has_perm("eventapp.delete_eventtype")
                    or request.user.has_perm("eventapp.add_eventtype")
                    or request.user.has_perm("eventapp.change_eventtype")
                )
        if view.__class__.__name__ == "CausesViewSet":
            if request.method == "GET":
                return request.user.has_perm("eventapp.view_causes")

            if (
                request.method == "POST"
                or request.method == "DELETE"
                or request.method == "PUT"
                or request.method == "PATCH"
            ):
                return (
                    request.user.has_perm("eventapp.delete_causes")
                    or request.user.has_perm("eventapp.add_causes")
                    or request.user.has_perm("eventapp.change_causes")
                )
        return False


class CanModifyOrViewPermissionUser(permissions.BasePermission):
    # userapp permissions
    def has_permission(self, request, view):
        user = request.user.id
        user_id = view.kwargs.get("pk")  # this is from url
        if view.__class__.__name__ == "UserViewSet":
            if request.method == "GET":# only user can see his/her profile
                return (
                    request.user.has_perm("userapp.view_user") or str(user) == user_id
                )
            if request.method == "POST":
                #everyone can create user but is it true? 
                return True
            if request.method in ["DELETE", "PUT", "PATCH"]:
                return (
                    request.user.has_perm("userapp.delete_user")
                    or request.user.has_perm("userapp.add_user")
                    or request.user.has_perm("userapp.change_user")# who have permission 
                    or str(user) == user_id# or users themselfs
                )
        return str(user) == user_id
