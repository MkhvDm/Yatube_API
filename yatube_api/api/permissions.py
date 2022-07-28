from rest_framework.permissions import SAFE_METHODS, BasePermission

# class ReadOnly(BasePermission):
#     message = 'Необходима авторизация.'
#
#     def has_permission(self, request, view):
#         if request.method in SAFE_METHODS:
#             return True
#         return False


class IsAuthorOrReadOnly(BasePermission):
    """Allows access only to author user."""
    message = ''

    def has_permission(self, request, view):
        self.message = 'Необходима авторизация.'
        return (
            request.method in SAFE_METHODS or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        self.message = 'Необходима авторство.'
        if request.method in SAFE_METHODS:
            return True
        return request.user == obj.author
