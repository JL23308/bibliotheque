from django.urls import path, include
from . import views
from emprunts.views import EmpruntViewSet, AvisViewSet
from rest_framework_nested import routers

app_name = 'livres'

livreRouter = routers.DefaultRouter()
livreRouter.register(r'livres', views.LivreViewSet,basename='livres')
domains_router = routers.NestedSimpleRouter(livreRouter, r'livres', lookup='livres')
domains_router.register(r'categories', views.CategorieViewSet, basename='livres-categories')
domains_router.register(r'avis', AvisViewSet, basename='livres-avis')
domains_router.register(r'emprunts', EmpruntViewSet, basename='livres-emprunts')


auteurRouter = routers.DefaultRouter()
auteurRouter.register(r'auteurs', views.AuteurViewSet, basename='auteur')
domains2_router = routers.NestedSimpleRouter(auteurRouter, r'auteurs', lookup='auteurs')
domains2_router.register(r'livres', views.LivreViewSet, basename='auteurs-livres')

categorieRouter = routers.DefaultRouter()
categorieRouter.register(r'categories', views.CategorieViewSet, basename='categorie')
domains3_router = routers.NestedSimpleRouter(categorieRouter, r'categories', lookup='categories')
domains3_router.register(r'livres', views.LivreViewSet, basename='categories-livres')


urlpatterns = [
    path(r'', include(livreRouter.urls)),
    path(r'', include(domains_router.urls)),
    path(r'', include(auteurRouter.urls)),
    path(r'', include(domains2_router.urls)),
    path(r'', include(categorieRouter.urls)),
    path(r'', include(domains3_router.urls)),
]

