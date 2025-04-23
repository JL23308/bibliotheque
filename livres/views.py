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
    queryset = Livre.objects.all()
    serializer_class = LivreSerializer
    permission_classes = [IsCreateurOrReadOnly, permissions.IsAuthenticatedOrReadOnly]
    filterset_class = LivreFilterSet
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]   
    pagination_class = LivrePagination
    ordering_fields = ['titre', 'date_publication', 'auteur__nom']


    @extend_schema(
        parameters=[
            OpenApiParameter(name='request', required=True),
            OpenApiParameter(name='auteurs_pk', required=False, description='')
        ],
        # override default docstring extraction
        description='More descriptive text',
        # provide Authentication class that deviates from the views default
        auth=None,
        # change the auto-generated operation name
        operation_id=None,
        # or even completely override what AutoSchema would generate. Provide raw Open API spec as Dict.
        operation=None,
        # attach request/response examples to the operation.
        examples=[
            OpenApiExample(
                'Example 1',
                description='longer description',
                value=""
            ),
        ],
    )   
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

    @action(detail=True, methods=['patch', 'put'], url_path='add-auteur/(?P<auteur_pk>\d+)')
    def add_auteur(self, request, pk=None, auteur_pk=None):
        livre = self.get_object()
        auteur = get_object_or_404(Auteur, pk=auteur_pk)
        livre.auteurs.add(auteur)
        return Response({'status': 'auteur added'})
    
    @action(detail=True, methods=['patch', 'put'], url_path='remove-auteur/(?P<auteur_pk>\d+)')
    def remove_auteur(self, request, pk=None, auteur_pk=None):
        livre = self.get_object()
        auteur = get_object_or_404(Auteur, pk=auteur_pk)
        livre.auteurs.remove(auteur)
        return Response({'status': 'auteur removed'})

    @action(detail=True, methods=['patch', 'put'], url_path='add-categorie/(?P<categorie_pk>\d+)')
    def add_categorie(self, request, pk=None, categorie_pk=None):
        livre = self.get_object()
        categorie = get_object_or_404(Categorie, pk=categorie_pk)
        livre.categorie.add(categorie)
        return Response({'status': 'categorie added'})
    
    @action(detail=True, methods=['patch', 'put'], url_path='remove-categorie/(?P<categorie_pk>\d+)')
    def remove_categorie(self, request, pk=None, categorie_pk=None):
        livre = self.get_object()
        categorie = get_object_or_404(Categorie, pk=categorie_pk)
        livre.categorie.remove(categorie)
        return Response({'status': 'categorie removed'})
    
    def get_permissions(self):
        return super().get_permissions()

class CategorieViewSet(viewsets.ModelViewSet):

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
    queryset = Auteur.objects.all()
    serializer_class = AuteurSerializer
    
