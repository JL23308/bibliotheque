from rest_framework import permissions
from livres.models import Livre

class IsCreateurOrReadOnly(permissions.BasePermission):
  
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:    
            return True

        return obj.createur_id == request.user.id
    
    def has_permission(self, request, view):
        if request.data.get('isbn'):
            livre = Livre.objects.filter(isbn=request.data.get('isbn'))
            if livre :
                return livre[0].createur_id == request.user.id
            return True
        return super().has_permission(request, view)
                