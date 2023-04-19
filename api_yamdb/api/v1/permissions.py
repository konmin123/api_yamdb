from rest_framework import permissions


class IsAdminOrSuperuser(permissions.BasePermission):
    """
    Права доступа для администратора или суперюзера.
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_superuser or request.user.role == 'admin'
        return False


class IsAdminSuperuserUserOrReadOnly(permissions.BasePermission):
    """
    Права доступа для админа, модератера, суперюзера и автора.
    """

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.role in ['admin', 'moderator']
                or request.user.is_superuser
                or obj.author == request.user)


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Права доступа для админа, суперюзера или чтение.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == 'admin' or request.user.is_superuser
        return request.method in permissions.SAFE_METHODS
