from rest_framework.permissions import BasePermission


class IsVerified(BasePermission):
    """
    Custom permission to only allow verified users to access the view.
    """

    def has_permission(self, request, view):
        return request.user.is_verified


class IsVerifiedOrReadOnly(BasePermission):
    """
    Custom permission to only allow verified users to edit, but allow read-only access for all.
    """

    def has_permission(self, request, view):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True
        return request.user.is_verified
