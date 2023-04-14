from rest_framework import permissions


class IsAdminOrSuperuser(permissions.BasePermission):
    """Доступ только администратору или суперюзеру"""
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            user = request.user
            return user.is_superuser or user.role == 'admin'
        return False


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
