from rest_framework import permissions

class CanCreateDeleteUpdatePermission(permissions.BasePermission):
    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):

        if view.__class__.__name__ == "CompanyViewSet":
             return (
            request.user.has_perm('basedataapp.delete_company') or
            request.user.has_perm('basedataapp.add_company') or 
            request.user.has_perm('basedataapp.change_company')
        )
        if view.__class__.__name__ == "StructureViewSet":
             return (
            request.user.has_perm('basedataapp.delete_Structure') or
            request.user.has_perm('basedataapp.add_Structure') or 
            request.user.has_perm('basedataapp.change_Structure')
        )
        if view.__class__.__name__ == "ActivityNatureViewSet":
             return (
            request.user.has_perm('basedataapp.delete_activitynature') or
            request.user.has_perm('basedataapp.add_activitynature') or 
            request.user.has_perm('basedataapp.change_activitynature')
        )
        if view.__class__.__name__ == "WorkTypeViewSet":
             return (
            request.user.has_perm('basedataapp.delete_worktype') or
            request.user.has_perm('basedataapp.add_worktype') or 
            request.user.has_perm('basedataapp.change_worktype')
        )
        if view.__class__.__name__ == "WorkViewSet":
             return (
            request.user.has_perm('basedataapp.delete_work') or
            request.user.has_perm('basedataapp.add_work') or 
            request.user.has_perm('basedataapp.change_work')
        )
        if view.__class__.__name__ == "StructureTypeViewSet":
             return (
            request.user.has_perm('basedataapp.delete_structuretype') or
            request.user.has_perm('basedataapp.add_structuretype') or 
            request.user.has_perm('basedataapp.change_structuretype')
        )
        if view.__class__.__name__ == "InstallationViewSet":
             return (
            request.user.has_perm('basedataapp.delete_installation') or
            request.user.has_perm('basedataapp.add_installation') or 
            request.user.has_perm('basedataapp.change_installation')
        )
        return False
        # Check if the user has the necessary permissions to delete or update or create
       