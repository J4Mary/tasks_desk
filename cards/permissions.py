from rest_framework import permissions


class CreatedByAccessPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        ALLOWED_METHODS = ['PUT', 'PATCH']
        if request.method in ALLOWED_METHODS and obj.created_by == request.user:
            return True
        return request.user.is_superuser
