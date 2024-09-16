# books/permissions.py
from rest_framework.permissions import BasePermission

class IsSuperAdminOrPermittedUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'SuperAdmin':  # SuperAdmin can view all
            return True
        return request.user.is_authenticated  # Other roles need to be authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'SuperAdmin':
            return True
        return request.user in obj.permitted_users.all()
