from rest_framework import permissions


class OnlyUserAndStaffPermission(permissions.BasePermission):
    """
    Anonymous users have no permissions.
    Authenticated users can access to datas.
    Staff users can access, edit and add datas.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated

        if request.method in ('POST', 'DELETE', 'PUT', 'PATCH'):
            return request.user and request.user.is_staff

        return False


class PostByClientAndGetByUserPermission(permissions.BasePermission):
    """
    Anonymous users can add datas.
    Authenticated users can access to datas.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated

        if request.method in ('POST', 'DELETE', 'PUT', 'PATCH'):
            return not (request.user and request.user.is_authenticated)

        return False

