from rest_framework import permissions


class IsAdminSuperuserUserOrReadOnly(permissions.BasePermission):
    """Права на изменения для админа, суперюзера и автора
    для отзывов и комментариев."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.role in ['admin', 'moderator']
            or request.user.is_superuser
            or obj.author == request.user
        )
