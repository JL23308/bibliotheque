from rest_framework import permissions
from livres.models import Livre

class IsCreateurOrReadOnly(permissions.BasePermission):
  
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:    
            return True
        
        return obj.createur_id == request.user.id
    
    def __str__(self):
        return "You must be the createur to edit a livre, else you can read it"