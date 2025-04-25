from rest_framework import permissions

class IsAdminOrMembre(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return obj.membre.user.id == request.user.id