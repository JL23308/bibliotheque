from rest_framework import permissions
from django.contrib.auth.models import AnonymousUser

class IsAdminOrMembreToBookOrShareOpinion(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        
        if request.method == 'POST':
            try:
                return request.user.membre
            except:
                return False
            
        return True 
   
class IsAdminOrEmpruntBelongsToMember(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
    
        if obj.membre:
            return obj.membre.user.id == request.user.id  
        
        return True
    
class IsAdminOrAvisBelongsToMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            if obj.membre:
                return obj.membre.user.id == request.user.id  
        
        return True
    