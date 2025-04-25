from django.urls import path, include
from . import views
from livres.views import LivreViewSet
from rest_framework_nested import routers

app_name = 'livres'

#pas d'intêret à mettre des nested routers pour les emprunts et avis je pense

empruntsRouter = routers.SimpleRouter()
empruntsRouter.register(r'emprunts', views.EmpruntViewSet,basename='emprunts')

membresRouter = routers.SimpleRouter()
membresRouter.register(r'membres', views.MembreViewSet,basename='membres')
domains_router = routers.NestedSimpleRouter(membresRouter, r'membres', lookup='membres')
domains_router.register(r'emprunts', views.EmpruntViewSet, basename='membres-emprunts')
domains_router.register(r'avis', views.AvisViewSet, basename='membres-avis')

avisRouter = routers.SimpleRouter()
avisRouter.register(r'avis', views.AvisViewSet,basename='avis')

urlpatterns = [
    path(r'', include(empruntsRouter.urls)),
    path(r'', include(membresRouter.urls)),
    path(r'', include(domains_router.urls)),
    path(r'', include(avisRouter.urls)),
]
