from django.shortcuts import render, redirect, get_object_or_404
from django.core.cache import cache

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, viewsets, filters, status
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from .permissions import *
from api.pagination import *

from .serializers import * 
from .models import *
from .filters import *

# Create your views here.

class LivreViewSet(viewsets.ModelViewSet):
    """
        ViewSet for the object Livre with CRUD methods
    """

    queryset = Livre.objects.all()
    serializer_class = LivreSerializer
    permission_classes = [IsCreateurOrReadOnly, permissions.IsAuthenticatedOrReadOnly]
    filterset_class = LivreFilterSet
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]   
    pagination_class = LivrePagination
    ordering_fields = ['titre', 'date_publication', 'auteur__nom']

    def create(self, request, auteurs_pk=None, categories_pk=None):
        serializer = LivreSerializer(data=request.data)
        if(serializer.is_valid()):
            if auteurs_pk:
                auteur = get_object_or_404(Auteur, pk=auteurs_pk)
                serializer.save(auteur=auteur, createur=request.user)
            elif categories_pk:
                categorie = Categorie.objects.filter(pk=categories_pk)
                serializer.save(categorie=categorie, createur=request.user)    
            else :
                serializer.save(createur=request.user)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request, auteurs_pk=None, categories_pk=None):

        cache_key = 'my_unique_key' # needs to be unique
        cache_time = 86400 # time in seconds for cache to be valid
        livres = cache.get(cache_key) # returns None if no key-value pair
        if not livres:
            livres = None
            if auteurs_pk:
                livres = self.paginate_queryset(self.filter_queryset(self.get_queryset().filter(auteur=auteurs_pk)))
            elif categories_pk:
                livres = self.paginate_queryset(self.filter_queryset(self.get_queryset().filter(categorie=categories_pk)))
            else:
                return super().list(request) #marche pas pour les caches
            
            cache.set(cache_key, livres, cache_time)
        
        #livres = self.paginate_queryset(self.filter_queryset(livres))
        serializer = self.get_serializer(livres, many=True)
        return self.get_paginated_response(serializer.data)
    """
        return JsonResponse(data, safe=False)

        return self.get_paginated_response(serializer.data, status=status.HTTP_200_OK)
    """

    """
        Method that sets an Auteur to a Livre

        param:
            parameters are set in the url (example)
            - int pk, id of the Livre
            - int auteurs_pk, id of the Auteur
        return: 
            JSON response that contains a message that confirms the Auteur was set 
            or 404 error if the Auteur was not found

        example: 
            auteur1 = Auteur.objects.create(nom=SITHI, prenom='JL', date_naissance='2025-07-21')
            livre1 = Livre.objects.create(titre='titre1', date_publication='2025-01-01', isbn='6756786273879')
            auteur1.save()
            livre1.save()

            put /livres/1/set-auteur/1/
            response : {'status': 'auteur added'}
    """
    @action(detail=True, methods=['patch', 'put'], url_path='set-auteur/(?P<auteur_pk>\d+)')
    def set_auteur(self, request, pk=None, auteur_pk=None):
        livre = self.get_object()
        auteur = get_object_or_404(Auteur, pk=auteur_pk)
        livre.auteur = auteur
        livre.full_clean()
        livre.save()
        return Response({'status': 'auteur added'}, status=status.HTTP_200_OK)
    

    """
        Method that removes an Auteur from Livre

        param:
            parameters are set in the url (example)
            - int pk, id of the Livre
            - int auteurs_pk, id of the Auteur
        return: 
            JSON response that contains a message that confirms the Auteur was removed 
            or 404 error if the Auteur was not found

        example: 
            auteur1 = Auteur.objects.create(nom=SITHI, prenom='JL', date_naissance='2025-07-21')
            livre1 = Livre.objects.create(titre='titre1', date_publication='2025-01-01', isbn='6756786273879', auteur=auteur1)
            auteur1.save()
            livre1.save()

            put /livres/1/remove-auteur/1/
            response : {'status': 'auteur removed'}
    """
    @action(detail=True, methods=['patch', 'put'], url_path='remove-auteur/(?P<auteur_pk>\d+)')
    def remove_auteur(self, request, pk=None, auteur_pk=None):
        livre = self.get_object()
        auteur = get_object_or_404(Auteur, pk=auteur_pk)
        livre.auteur = None
        livre.full_clean()
        livre.save()
        return Response({'status': 'auteur removed'}, status=status.HTTP_200_OK)

    """
        Method that adds a Categorie to a Livre

        param:
            parameters are set in the url (example)
            - int pk, id of the Livre
            - int categories_pk, id of the Auteur
        return: 
            JSON response that contains a message that confirms the Categorie was added 
            or 404 error if the Categorie was not found

        example: 
            categorie1 = Categorie.objects.create(nom='horreur', description='fait peur')
            livre1 = Livre.objects.create(titre='titre1', date_publication='2025-01-01', isbn='6756786273879')
            categorie1.save()
            livre1.save()

            put /livres/1/add-categorie/1/
            response : {'status': 'categorie added'}
    """
    @action(detail=True, methods=['patch', 'put'], url_path='add-categorie/(?P<categorie_pk>\d+)')
    def add_categorie(self, request, pk=None, categorie_pk=None):
        livre = self.get_object()
        categorie = get_object_or_404(Categorie, pk=categorie_pk)
        livre.categorie.add(categorie)
        return Response({'status': 'categorie added'}, status=status.HTTP_200_OK)
    
    """
        Method that removes a Categorie of a Livre

        param:
            parameters are set in the url (example)
            - int pk, id of the Livre
            - int categories_pk, id of the Auteur
        return: 
            JSON response that contains a message that confirms the Categorie was removed 
            or 404 error if the Categorie was not found

        example: 
            categorie1 = Categorie.objects.create(nom='horreur', description='fait peur')
            livre1 = Livre.objects.create(titre='titre1', date_publication='2025-01-01', isbn='6756786273879')
            livre1.categorie.add(categorie)
            categorie1.save()
            livre1.save()

            put /livres/1/remove-categorie/1/
            response : {'status': 'categorie removed'}
    """
    @action(detail=True, methods=['patch', 'put'], url_path='remove-categorie/(?P<categorie_pk>\d+)')
    def remove_categorie(self, request, pk=None, categorie_pk=None):
        livre = self.get_object()
        categorie = get_object_or_404(Categorie, pk=categorie_pk)
        livre.categorie.remove(categorie)
        return Response({'status': 'categorie removed'}, status=status.HTTP_200_OK)
    
    def get_permissions(self):
        return super().get_permissions()

class CategorieViewSet(viewsets.ModelViewSet):
    """
        ViewSet for the object Categorie with CRUD methods
    """
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer

    def list(self, request, livres_pk=None):
        categories = None
        if livres_pk:
            categories = self.queryset.filter(livre=livres_pk)
        else:
            return super().list(request)
    
        serializer = CategorieSerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class AuteurViewSet(viewsets.ModelViewSet):
    """
        ViewSet for the object Auteur with CRUD methods
    """
    queryset = Auteur.objects.all()
    serializer_class = AuteurSerializer
    
