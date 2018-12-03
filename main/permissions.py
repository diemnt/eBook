from rest_framework import permissions


class RetrieveAndIsAuthenticated(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return (view.action in ['retrieve', 'list']
                and super(RetrieveAndIsAuthenticated, self).has_permission(request, view))


class UpdateAndIsAuthenticated(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return (view.action in ['update', 'partial_update']
                and super(UpdateAndIsAuthenticated, self).has_permission(request, view))


class DeleteAndIsAuthenticated(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return (view.action == 'destroy'
                and super(DeleteAndIsAuthenticated, self).has_permission(request, view))


