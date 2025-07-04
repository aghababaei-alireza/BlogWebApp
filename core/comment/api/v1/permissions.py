from rest_framework.permissions import BasePermission


class IsAuthorOrReadOnly(BasePermission):
    """
    Custom permission to only allow authors of a comment to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Allow read-only access for all users
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True
        # Allow editing or deleting only if the user is the author of the comment
        return obj.author == request.user
