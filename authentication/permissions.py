from rest_framework.permissions import (
    BasePermission
)


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
            and request.user.role ==
            'SUPER_USER'
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


class IsMemberOrAbove(
    BasePermission
):

    def has_permission(
        self,
        request,
        view
    ):

        return (
            request.user.is_authenticated
        )


class IsAdminOrOwner(
    BasePermission
):

    def has_permission(
        self,
        request,
        view
    ):

        return request.user.is_authenticated

    def has_object_permission(
        self,
        request,
        view,
        obj
    ):

        if request.user.role in [
            'SUPER_USER',
            'ADMIN_USER',
            'HIGH_PRIVILEGE_USER'
        ]:
            return True

        for field in [
            'author',
            'member',
            'user',
            'uploaded_by',
            'recorded_by',
            'requested_by',
        ]:
            owner = getattr(obj, field, None)
            if owner == request.user:
                return True

        post = getattr(obj, 'post', None)
        if post and post.author == request.user:
            return True

        comment = getattr(obj, 'comment', None)
        if comment and comment.author == request.user:
            return True

        return False