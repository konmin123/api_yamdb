from rest_framework import permissions
from api.models import User


class IsAdmin(permissions.BasePermission):
    """Доступ только администратору"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class IsPersonalOnly(permissions.BasePermission):
    """Доступ только администратору"""
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return User.objects.filter(username=request.user.username)
