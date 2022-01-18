from rest_framework.permissions import BasePermission, IsAdminUser, IsAuthenticated


class IsAuthorPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user == obj.owner or request.user.is_staff


class PermissionMixin:
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', ]:
            permissions = [IsAdminUser, ]
        else:
            permissions = [IsAuthenticated, ]
        return [permission() for permission in permissions]