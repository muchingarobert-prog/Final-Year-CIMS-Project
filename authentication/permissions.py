from rest_framework.permissions import BasePermission


class IsSuperUser(
    BasePermission
):

    def has_permission(
        self,
        request,
        view
    ):

        return (
            request.user.is_authenticated
            and request.user.role == 'SUPER_USER'
        )


class IsAdminUserRole(
    BasePermission
):

    def has_permission(
        self,
        request,
        view
    ):

        return (
            request.user.is_authenticated
            and request.user.role in [
                'SUPER_USER',
                'ADMIN_USER'
            ]
        )


class IsHighPrivilegeOrAbove(
    BasePermission
):

    def has_permission(
        self,
        request,
        view
    ):

        return (
            request.user.is_authenticated
            and request.user.role in [
                'SUPER_USER',
                'ADMIN_USER',
                'HIGH_PRIVILEGE_USER'
            ]
        )