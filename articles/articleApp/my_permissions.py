from rest_framework import permissions

class IsConfirmed(permissions.BasePermission):
    message = 'Not Allowed for Unconfirmed Accounts'

    def has_permission(self, request, view):
        return request.user.is_confirmed