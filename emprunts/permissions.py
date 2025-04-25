from rest_framework import permissions

class IsAdminOrMembre(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return True
        
    
    """
    plus tard quand je serai sur les nested routers des membres
    def has_permission(self, request, view):
        dd(request)
    """