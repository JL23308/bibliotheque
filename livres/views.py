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
from emprunts.models import Emprunt

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

    def create(self, request, categories_pk=None):
        serializer = LivreSerializer(data=request.data)
        if(serializer.is_valid()):
            if categories_pk:
                categorie = Categorie.objects.filter(pk=categories_pk)
                serializer.save(categorie=categorie, createur=request.user)    
            else :
                serializer.save(createur=request.user)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request, categories_pk=None):
        cache_key = 'livres-list-%s' % (categories_pk)
        for key, item in request.query_params.items():
            cache_key += "-%s-%s" % (key, item)
        
        cache_time = 86400 # time in seconds for cache to be valid
        #cache.set(cache_key, None, cache_time)   
        data = cache.get(cache_key) # returns None if no key-value pair    
       
        if data:
            self.paginator.page = data[0]
            self.paginator.request = request
            self.paginator.display_page_controls = True
            return self.get_paginated_response(data[1]) 
            
        if categories_pk:
            livres = self.paginate_queryset(self.filter_queryset(self.get_queryset().filter(categorie=categories_pk)))
        else:
            livres = self.paginate_queryset(self.filter_queryset(self.get_queryset()))
       
        serializer = self.get_serializer(livres, many=True)
        cache.set(cache_key, [self.paginator.page, serializer.data], cache_time)
        return self.get_paginated_response(serializer.data)
    
    def retrieve(self, request, pk, categories_pk=None):
        
        cache_key = 'livres-%s' % (pk)
        cache_time = 86400 # time in seconds for cache to be valid
        #cache.set(cache_key, None, cache_time)   
        data = cache.get(cache_key) # returns None if no key-value pair   

        if not data:
            livre = self.queryset.get(pk=pk)
            serializer = LivreSerializer(livre)
            cache.set(cache_key, serializer.data, cache_time)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(data, status=status.HTTP_200_OK)

    @extend_schema(
        description='Method that sets an Auteur to a Livre',
        examples=[
            OpenApiExample(
                'Example 1',
                description='method put on /livres/1/set-auteur/1/',
                value="{'status': 'auteur added'}"
            ),
        ],
    )
    @action(detail=True, methods=['patch', 'put'], url_path='set-auteur/(?P<auteur_pk>\d+)')
    def set_auteur(self, request, pk=None, auteur_pk=None):
        livre = self.get_object()
        auteur = get_object_or_404(Auteur, pk=auteur_pk)
        livre.auteur = auteur
        livre.full_clean()
        livre.save()
        return Response({'status': 'auteur added'}, status=status.HTTP_200_OK)
    
    @extend_schema(
        description='Method that removes an Auteur from Livre',
        examples=[
            OpenApiExample(
                'Example 1',
                description='method put on /livres/1/remove-auteur/1/',
                value="{'status': 'auteur removed'}"
            ),
        ],
    )
    @action(detail=True, methods=['patch', 'put'], url_path='remove-auteur/(?P<auteur_pk>\d+)')
    def remove_auteur(self, request, pk=None, auteur_pk=None):
        livre = self.get_object()
        auteur = get_object_or_404(Auteur, pk=auteur_pk)
        livre.auteur = None
        livre.full_clean()
        livre.save()
        return Response({'status': 'auteur removed'}, status=status.HTTP_200_OK)

    @extend_schema(
        description='Method that sets an Emprunt to a Livre',
        examples=[
            OpenApiExample(
                'Example 1',
                description='method put on /livres/1/set-emprunt/1/',
                value="{'status': 'emprunt added'}"
            ),
        ],
    )
    @action(detail=True, methods=['patch', 'put'], url_path='set-emprunt/(?P<emprunt_pk>\d+)')
    def set_emprunt(self, request, pk=None, emprunt_pk=None):
        livre = self.get_object()
        emprunt = get_object_or_404(Emprunt, pk=emprunt_pk)
        if not emprunt.retourne:
            already_booked = Emprunt.objects.filter(retourne=None, livre=livre)
            if already_booked:
                return Response({'status': 'this book is not available'}, status=status.HTTP_400_BAD_REQUEST)
            
        livre.emprunt_set.add(emprunt)
        livre.full_clean()
        livre.save()
        return Response({'status': 'emprunt added'}, status=status.HTTP_200_OK)
    
    @extend_schema(
        description='Method that removes an Emprunt from a Livre',
        examples=[
            OpenApiExample(
                'Example 1',
                description='method put on /livres/1/remove-emprunt/1/',
                value="{'status': 'emprunt removed'}"
            ),
        ],
    )
    @action(detail=True, methods=['patch', 'put'], url_path='remove-emprunt/(?P<emprunt_pk>\d+)')
    def remove_emprunt(self, request, pk=None, emprunt_pk=None):
        livre = self.get_object()
        emprunt = get_object_or_404(Emprunt, pk=emprunt_pk)
        livre.emprunt_set.remove(emprunt)
        livre.full_clean()
        livre.save()
        return Response({'status': 'emprunt removed'}, status=status.HTTP_200_OK)
    
   
    @extend_schema(
        description='Method that adds a Categorie to a Livre',
        examples=[
            OpenApiExample(
                'Example 1',
                description='method put on /livres/1/add-categorie/1/',
                value="{'status': 'categorie added'}"
            ),
        ],
    )
    @action(detail=True, methods=['patch', 'put'], url_path='add-categorie/(?P<categorie_pk>\d+)')
    def add_categorie(self, request, pk=None, categorie_pk=None):
        livre = self.get_object()
        categorie = get_object_or_404(Categorie, pk=categorie_pk)
        livre.categorie.add(categorie)
        return Response({'status': 'categorie added'}, status=status.HTTP_200_OK)
    
    @extend_schema(
        description='Method that removes a Categorie from a Livre',
        examples=[
            OpenApiExample(
                'Example 1',
                description='method put on /livres/1/remove-categorie/1/',
                value="{'status': 'categorie removed'}"
            ),
        ],
    )
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
    permission_classes = [permissions.IsAdminUser]
    filterset_class = CategorieFilterSet
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]   
    pagination_class = CategoriePagination
    ordering_fields = ['livre__titre', 'livre__date_publication', 'date_naissance']


    def list(self, request, livres_pk=None):
        cache_key = 'categories-list-%s' % (livres_pk)    
        for key, item in request.query_params.items():
            cache_key += "-%s-%s" % (key, item)
        cache_time = 86400 # time in seconds for cache to be valid
        data = cache.get(cache_key) # returns None if no key-value pair    

        if data:
            self.paginator.page = data[0]
            self.paginator.request = request
            self.paginator.display_page_controls = True
            return self.get_paginated_response(data[1]) 
        
        if livres_pk:
            #categories = self.queryset.filter(livre=livres_pk)
            categories = self.paginate_queryset(self.filter_queryset(self.get_queryset().filter(livre=livres_pk)))
        else:
            categories = self.paginate_queryset(self.filter_queryset(self.get_queryset()))
        
        serializer = self.get_serializer(categories, many=True)
        cache.set(cache_key, [self.paginator.page, serializer.data], cache_time)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, pk, livres_pk=None):
        
        cache_key = 'categories-%s' % (pk)
        cache_time = 86400 # time in seconds for cache to be valid
        #cache.set(cache_key, None, cache_time)   
        data = cache.get(cache_key) # returns None if no key-value pair   

        if not data:
            categorie = self.queryset.get(pk=pk)
            serializer = CategorieSerializer(categorie)
            cache.set(cache_key, serializer.data, cache_time)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(data, status=status.HTTP_200_OK)
    
class AuteurViewSet(viewsets.ModelViewSet):
    """
        ViewSet for the object Auteur with CRUD methods
    """
    queryset = Auteur.objects.all()
    serializer_class = AuteurSerializer
    permission_classes = [permissions.IsAdminUser]
    filterset_class = AuteurFilterSet
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]   
    pagination_class = AuteurPagination
    ordering_fields = ['nom', 'prenom', 'date_naissance']

    def list(self, request):  
        cache_key = 'auteurs-list'    
        for key, item in request.query_params.items():
            cache_key += "-%s-%s" % (key, item)
        cache_time = 86400 # time in seconds for cache to be valid
        data = cache.get(cache_key) # returns None if no key-value pair    

        if data:
            self.paginator.page = data[0]
            self.paginator.request = request
            self.paginator.display_page_controls = True
            return self.get_paginated_response(data[1]) 
        
        
        categories = self.paginate_queryset(self.filter_queryset(self.get_queryset()))
        
        serializer = self.get_serializer(categories, many=True)
        cache.set(cache_key, [self.paginator.page, serializer.data], cache_time)
        return self.get_paginated_response(serializer.data)



    def retrieve(self, request, pk, livres_pk=None):
        
        cache_key = 'auteurs-%s' % (pk)
        cache_time = 86400 # time in seconds for cache to be valid
        #cache.set(cache_key, None, cache_time)   
        data = cache.get(cache_key) # returns None if no key-value pair   

        if not data:
            auteur = self.queryset.get(pk=pk)
            serializer = AuteurSerializer(auteur)
            cache.set(cache_key, serializer.data, cache_time)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(data, status=status.HTTP_200_OK)
    