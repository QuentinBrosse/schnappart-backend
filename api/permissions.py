from rest_framework import permissions
from .models import SearchResult


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


class IsOwnerOfSearchResultM2M(permissions.BasePermission):
    """
    For all methods, allow only the owner of the SearchResult
    (for many-to-many).
    """

    def has_permission(self, request, view):
        search_result_id = request.data.get('search_result', None)
        if not search_result_id:
            return True
        search_result = SearchResult.objects.get(pk=int(search_result_id))
        return search_result.search.project.user == request.user
