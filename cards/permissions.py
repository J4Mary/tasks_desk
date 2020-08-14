from rest_framework import permissions


class CreatedByAccessPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS'] and obj.created_by == request.user:
            return True
        elif request.method in ['PUT', 'PATCH'] and obj.created_by == request.user and obj.status < 4:
            return True
        return request.user.is_superuser

    def has_permission(self, request, view):
        if request.user.active:
            return True
        return request.user.is_superuser
