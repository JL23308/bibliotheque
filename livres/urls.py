from django.urls import path, include
from . import views
from rest_framework_nested import routers

livreRouter = routers.DefaultRouter()
livreRouter.register(r'livres', views.LivreViewSet)
domains_router = routers.NestedSimpleRouter(livreRouter, r'livres', lookup='livres')
domains_router.register(r'auteurs', views.AuteurViewSet, basename='livres-auteurs')
domains_router.register(r'categories', views.CategorieViewSet, basename='livres-categories')

auteurRouter = routers.DefaultRouter()
auteurRouter.register(r'auteurs', views.AuteurViewSet)
domains2_router = routers.NestedSimpleRouter(auteurRouter, r'auteurs', lookup='auteurs')
domains2_router.register(r'livres', views.LivreViewSet, basename='auteurs-livres')

categorieRouter = routers.DefaultRouter()
categorieRouter.register(r'categories', views.CategorieViewSet)
domains3_router = routers.NestedSimpleRouter(categorieRouter, r'categories', lookup='categories')
domains3_router.register(r'livres', views.LivreViewSet, basename='categories-livres')

urlpatterns = [
    path('livres', views.LivreViewSet.as_view({
        'get': 'list', 
        'delete': 'destroy',
        'post': 'create',
        'put': 'update'
        }), name='livres'),
    path(r'', include(livreRouter.urls),),
    path(r'', include(domains_router.urls)),
    path(r'', include(auteurRouter.urls)),
    path(r'', include(domains2_router.urls)),
    path(r'', include(categorieRouter.urls)),
    path(r'', include(domains3_router.urls)),
]

