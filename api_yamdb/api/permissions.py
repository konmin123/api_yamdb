from rest_framework import permissions


class IsAdminOrSuperuser(permissions.BasePermission):
    """Доступ только администратору или суперюзеру"""
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            user = request.user
            return user.is_superuser or user.role == 'admin'
        return False
