from rest_framework import permissions
from livres.models import Livre

class IsCreateurOrReadOnly(permissions.BasePermission):
  
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:    
            return True

        return obj.createur_id == request.user.id
    
    def has_permission(self, request, view):
        if request.data.get('isbn'):
            livre = Livre.objects.get(isbn=request.data.get('isbn'))
            return livre.createur_id == request.user.id
        
        return super().has_permission(request, view)
                