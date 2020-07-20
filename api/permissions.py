from rest_framework import permissions
from .models import School

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permission are allowed to any request,
        # so, we'll allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object
        return obj.user == request.user

class IsSchoolOwner(permissions.BasePermission):
    """
    Custom permission to check if the object belongs to the 
    logged in user's school.
    """

    def has_object_permission(self, request, view, obj):
        try:
            school = School.objects.get(user=request.user)
            return obj.school == school
        except Exception:
            return False