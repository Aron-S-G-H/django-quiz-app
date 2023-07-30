from rest_framework.permissions import BasePermission


class IsStaff(BasePermission):
    """
    Global permission check for if user is staff or not.
    """
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        else:
            return False
