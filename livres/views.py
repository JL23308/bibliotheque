from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, viewsets, filters
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

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

    def create(self, request, auteurs_pk=None, categories_pk=None):
        request.data.createur = request.user.id
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
        return Response(serializer.errors)
    
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
     
    def create(self, request, livres_pk=None):                
        serializer = CategorieSerializer(data=request.data)
        if serializer.is_valid():    
            if livres_pk:
                l = Livre.objects.filter(pk=livres_pk)
                serializer.save(livre=l)
            else:
                return super().create(request)
            return Response(serializer.data)
        return Response(serializer.errors)
    
class AuteurViewSet(viewsets.ModelViewSet):
    queryset = Auteur.objects.all()
    serializer_class = AuteurSerializer
    
