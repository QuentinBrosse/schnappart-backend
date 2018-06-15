from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    For all methods, allow only the owner of the object.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsOwnerOfSearchResult(permissions.BasePermission):
    """
    For all methods, allow only the owner of the SearchResult.
    """

    def has_object_permission(self, request, view, obj):
        return obj.search.project.user == request.user
