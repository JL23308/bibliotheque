from django.shortcuts import render, redirect
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
    ordering_fields = ['titre', 'data_publication', 'auteur__nom']

    def create(self, request, auteurs_pk=None, categories_pk=None):
        request.data.createur = request.user.id
        serializer = LivreSerializer(data=request.data)
        if(serializer.is_valid()):
            if auteurs_pk:
                auteur = Auteur.objects.get(pk=auteurs_pk)
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
            livres = self.paginate_queryset(self.filter_queryset(self.get_queryset()))
        
        serializer = self.get_serializer(livres, many=True)
        return self.get_paginated_response(serializer.data)

    def update(self, request, pk, auteurs_pk=None, categories_pk=None):
        livre = Livre.objects.get(pk=pk)
        serializer = LivreSerializer(instance=livre, data=request.data)
        if serializer.is_valid():
            if auteurs_pk:
                auteur = Auteur.objects.get(pk=auteurs_pk)
                serializer.save(auteur=auteur)
            elif categories_pk:
                categories = Categorie.objects.filter(pk=categories_pk)
                serializer.save(categorie=livre.categorie.all() | categories)
            else:
                serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def partial_update(self, request, pk, auteurs_pk=None, categories_pk=None):
        livre = Livre.objects.get(pk=pk)
        serializer = LivreSerializer(instance=livre, data=request.data)
        if serializer.is_valid():
            if auteurs_pk:
                auteur = Auteur.objects.get(pk=auteurs_pk)
                serializer.save(auteur=auteur)
            elif categories_pk:
                categories = Categorie.objects.filter(pk=categories_pk)
                serializer.save(categorie=livre.categorie.all() | categories)
            else:
                serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def destroy(self, request, pk, categories_pk=None):
        livre = Livre.objects.get(pk=pk)
        if categories_pk:
            serializer = LivreSerializer(instance=livre, data=request.data)
            if serializer.is_valid():
                serializer.save(categorie=livre.categorie.all().exclude(pk=categories_pk))
                return Response(serializer.data)
            return Response(serializer.errors)

        livre.delete()
        return redirect("/livres")
    
    def get_permissions(self):
        if self.action == 'update':
            permission_classes = [IsCreateurOrReadOnly]
        else:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]

class CategorieViewSet(viewsets.ModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    
    def list(self, request, livres_pk=None):
        categories = None
        if livres_pk:
            categories = self.queryset.filter(livre=livres_pk)
        else:
            categories = self.filter_queryset(self.get_queryset()).filter()
    
        serializer = CategorieSerializer(categories, many=True)
        return Response(serializer.data)
     
    def create(self, request, livres_pk=None):                
        serializer = CategorieSerializer(data=request.data)
        if serializer.is_valid():    
            if livres_pk:
                l = Livre.objects.filter(pk=livres_pk)
                serializer.save(livre=l)
            else:
                serializer.save()    
            return Response(serializer.data)
        return Response(serializer.errors)

    def update(self, request, pk, livres_pk=None):
        categorie = Categorie.objects.get(pk=pk)
        serializer = CategorieSerializer(instance=categorie, data=request.data)
        if serializer.is_valid():
            if livres_pk:
                livres = Livre.objects.filter(pk=livres_pk)
                serializer.save(livre=categorie.livre.all() | livres)
            else:
                serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def destroy(self, request,pk, livres_pk=None):
        categorie = Categorie.objects.get(pk=pk)
        if livres_pk:
            serializer = CategorieSerializer(instance=categorie, data=request.data)
            if serializer.is_valid():
                serializer.save(livre=categorie.livre.all().exclude(pk=livres_pk))
                return Response(serializer.data)
            return Response(serializer.errors)
        
        categorie.delete()
        return Response(status=204)

class AuteurViewSet(viewsets.ModelViewSet):
    queryset = Auteur.objects.all()
    serializer_class = AuteurSerializer

    def list(self, request, livres_pk=None):
        if livres_pk:
            auteurs = self.queryset.filter(livre=livres_pk)
        else:
            auteurs = self.filter_queryset(self.get_queryset()).filter()

        serializer = AuteurSerializer(auteurs, many=True)
        return Response(serializer.data)
    
