from rest_framework import permissions

class IsAdminOrMembre(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        
        if request.method in permissions.SAFE_METHODS:
            if obj.membre:
                return obj.membre.user.id == request.user.id  

        if request.method == 'delete':
            return obj.membre.user.id == request.user.id  

        return False
    
    def has_permission(self, request, view):
        return True
        dd(request)
   