from rest_framework.permissions import BasePermission, SAFE_METHODS


class ReadOnly(BasePermission):
    message = 'Необходима авторизация.'

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True


class IsAuthor(BasePermission):
    """Allows access only to author user."""
    message = 'Это действие доступно только автору.'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user == obj.author
