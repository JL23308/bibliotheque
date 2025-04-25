from rest_framework import permissions
from livres.models import Livre

class IsCreateurOrReadOnly(permissions.BasePermission):
  
    def has_object_permission(self, request, view, obj):
        dd
        if request.method in permissions.SAFE_METHODS:    
            return True

        return obj.createur_id == request.user.id

    def has_permission(self, request, view):
        dd(request)
        pass