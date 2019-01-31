from rest_framework import permissions


# Création d'une permission qui permet seulement au utilisateur authentifié d'accéder à la données et les membres staff peuvent modifé ou ajouter les données
class OnlyUserAndStaffPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated

        if request.method in ('POST', 'DELETE', 'PUT', 'PATCH'):
            return request.user and request.user.is_staff

        return False


# Création d'une permission qui permet seulement au utilisateur authentifi
class PostByClientAndGetByUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated

        if request.method in ('POST', 'DELETE', 'PUT', 'PATCH'):
            return not (request.user and request.user.is_authenticated)

        return False

