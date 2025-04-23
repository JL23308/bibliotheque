from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, viewsets, filters
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
        A ViewSet for the Livre object with CRUD methods
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
            
            return Response(serializer.data)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request, auteurs_pk=None, categories_pk=None):
        livres = None
        if auteurs_pk:
            livres = self.paginate_queryset(self.filter_queryset(self.get_queryset().filter(auteur=auteurs_pk)))
        elif categories_pk:
            livres = self.paginate_queryset(self.filter_queryset(self.get_queryset().filter(categorie=categories_pk)))
        else:
            return super().list(request)
        
        serializer = self.get_serializer(livres, many=True)
        return self.get_paginated_response(serializer.data)


    """
        Function that adds an Auteur to a Livre
        
        param:
        these params are set in the url.
        - int pk : id of the Livre
        - int auteur_pk : id of the Auteur
        
        retrun: JSON response that contains a message that confirms that the Auteur was added
        or a 404 error if the Auteur doesn't exist

        example: 
        auteur1 = Auteur.objects.create(titre=titre1, date_publication=2025-01-01)
        livre1 = Livre.objects.create(titre=titre, date_publication=2025-01-01, isbn=1239237429823)

        put: /livre/1/add-auteur/1/ 
        response: 
        {
            status: auteur added
        } 
    """
    @action(detail=True, methods=['patch', 'put'], url_path='add-auteur/(?P<auteur_pk>\d+)')
    def set_auteur(self, request, pk=None, auteur_pk=None):
        livre = self.get_object()
        auteur = get_object_or_404(Auteur, pk=auteur_pk)
        livre.auteur = auteur
        livre.full_clean()
        livre.save()
        return Response({'status': 'auteur added'})
    
    """
        Function that removes an Auteur of a Livre
        
        param:
        these params are set in the url. 
        - int pk : id of the Livre
        - int auteur_pk : id of the Auteur
        
        retrun: JSON response that contains a message that confirms that the Auteur was removed
        or a 404 error if the Auteur doesn't exist

        example: 
        auteur1 = Auteur.objects.create(titre=titre1, date_publication=2025-01-01)
        livre1 = Livre.objects.create(titre=titre, date_publication=2025-01-01, isbn=1239237429823, auteur=auteur1)

        put: /livre/1/remove-auteur/1/ 
        response: 
        {
            status: auteur removed
        } 
    """
    @action(detail=True, methods=['patch', 'put'], url_path='remove-auteur/(?P<auteur_pk>\d+)')
    def remove_auteur(self, request, pk=None, auteur_pk=None):
        livre = self.get_object()
        auteur = get_object_or_404(Auteur, pk=auteur_pk)
        livre.auteur = None
        livre.full_clean()
        livre.save()
        return Response({'status': 'auteur removed'})

    """
        Function that adds an Categorie to a Livre
        
        param:
        these params are set in the url.
        - int pk : id of the Livre
        - int categorie_pk : id of the Categorie
        
        retrun: JSON response that contains a message that confirms that the Categorie was added
        or a 404 error if the Categorie doesn't exist

        example: 
        categorie1 = Categorie.objects.create(nom=horreur, description=fait peur)
        livre1 = Livre.objects.create(titre=titre, date_publication=2025-01-01, isbn=1239237429823)

        put: /livre/1/add-categorie/1/ 
        response: 
        {
            status: categorie added
        } 
    """
    @action(detail=True, methods=['patch', 'put'], url_path='add-categorie/(?P<categorie_pk>\d+)')
    def add_categorie(self, request, pk=None, categorie_pk=None):
        livre = self.get_object()
        categorie = get_object_or_404(Categorie, pk=categorie_pk)
        livre.categorie.add(categorie)
        return Response({'status': 'categorie added'})
    
    """
        Function that removes an Categorie of a Livre
        
        param:
        these params are set in the url.
        - int pk : id of the Livre
        - int categorie_pk : id of the Categorie
        
        retrun: JSON response that contains a message that confirms that the Categorie was removed
        or a 404 error if the Categorie doesn't exist

        example: 
        categorie1 = Categorie.objects.create(nom=horreur, description=fait peur)
        livre1 = Livre.objects.create(titre=titre, date_publication=2025-01-01, isbn=1239237429823)
        livre1.categorie.add(categorie)

        put: /livre/1/remove-categorie/1/ 
        response: 
        {
            status: categorie removed
        } 
    """
    @action(detail=True, methods=['patch', 'put'], url_path='remove-categorie/(?P<categorie_pk>\d+)')
    def remove_categorie(self, request, pk=None, categorie_pk=None):
        livre = self.get_object()
        categorie = get_object_or_404(Categorie, pk=categorie_pk)
        livre.categorie.remove(categorie)
        return Response({'status': 'categorie removed'})
    
    def get_permissions(self):
        return super().get_permissions()

class CategorieViewSet(viewsets.ModelViewSet):
    """
        A ViewSet for the Categorie object with CRUD methods
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
        return Response(serializer.data)
    
class AuteurViewSet(viewsets.ModelViewSet):
    """
        A ViewSet for the Auteur object with CRUD methods
    """
    queryset = Auteur.objects.all()
    serializer_class = AuteurSerializer
    
