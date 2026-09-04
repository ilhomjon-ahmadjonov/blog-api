from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrAdminDeleteOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if request.method in ['PUT', 'PATCH']:
            return obj.author == request.user

        if request.method == 'DELETE':
            if obj.author == request.user:
                return True
            if request.user.is_staff:
                return True
            return False

        return False


class IsCommentOwnerOrAdminDeleteOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if request.method in ['PUT', 'PATCH']:
            return obj.user == request.user

        if request.method == 'DELETE':
            if obj.user == request.user:
                return True
            if request.user.is_staff:
                return True
            return False

        return False