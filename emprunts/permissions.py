from rest_framework import permissions
from django.contrib.auth.models import AnonymousUser

class IsAdminOrMembre(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        
        if view.__class__.__name__ == 'EmpruntViewSet':
            if request.method in permissions.SAFE_METHODS:
                if obj.membre:
                    return obj.membre.user.id == request.user.id  
                
            if request.method == 'delete':
                return obj.membre.user.id == request.user.id  
        
        #====================================================

        if view.__class__.__name__ == 'AvisViewSet':
            if request.method in permissions.SAFE_METHODS:
                return True
            
            if type(request.user) != AnonymousUser:
                return obj.membre.user.id == request.user.id
            

        #====================================================
        
        return False
    
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
    
        if view.__class__.__name__ == 'EmpruntViewSet':
            if request.method in permissions.SAFE_METHODS and type(request.user) != AnonymousUser:
                return True
                
            if request.method == 'post':
                return request.user.membre
            
        #====================================================
        
        if view.__class__.__name__ == 'AvisViewSet':
            if request.method in permissions.SAFE_METHODS:
                return True
            
            if request.method == 'post':
                return request.user.membre
            

        return False
   