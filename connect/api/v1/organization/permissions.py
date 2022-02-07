from rest_framework import permissions

from connect.api.v1 import READ_METHODS, WRITE_METHODS


class OrganizationHasPermission(permissions.BasePermission):  # pragma: no cover
    def has_object_permission(self, request, view, obj):
        authorization = obj.get_user_authorization(request.user)
        if request.method in READ_METHODS and not request.user.is_authenticated:
            return authorization.can_read

        if request.user.is_authenticated:
            if request.method in READ_METHODS:
                return authorization.can_read
            if request.method in WRITE_METHODS:
                return authorization.can_write
            return authorization.is_admin
        return False


class OrganizationAdminManagerAuthorization(
    permissions.BasePermission
):  # pragma: no cover
    def has_object_permission(self, request, view, obj):
        authorization = obj.organization.get_user_authorization(request.user)
        return authorization.is_admin


class OrganizationHasPermissionBilling(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        authorization = obj.organization.get_user_authorization(request.user)
        return authorization.can_contribute_billing
