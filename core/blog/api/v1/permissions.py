from rest_framework.permissions import BasePermission


class IsVerifiedOrReadOnly(BasePermission):
    """
    Custom permission to only allow verified users to edit objects.
    Unverified users can only read objects.
    """

    def has_permission(self, request, view):
        # Allow read-only access for unauthenticated users
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        # Allow access for authenticated and verified users
        return request.user.is_verified


class IsSuperuserOrReadOnly(BasePermission):
    """
    Custom permission to only allow superusers to edit objects.
    Other users can only read the object.
    """

    def has_permission(self, request, view):
        # Allow read-only access for unauthenticated users
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        # Allow access for superusers
        return request.user and request.user.is_superuser


class IsAuthorOrReadOnly(BasePermission):
    """
    Custom permission to only allow authors of an object to edit it.
    Other users can only read the object.
    """

    def has_object_permission(self, request, view, obj):
        # Allow read-only access for unauthenticated users
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        # Allow access for the author of the object
        return obj.author == request.user
