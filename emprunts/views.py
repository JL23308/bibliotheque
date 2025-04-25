from django.shortcuts import render, get_object_or_404
from django.core.cache import cache
from rest_framework import filters, viewsets, status, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from .models import *
from .serializers import *
from .permissions import *
from api.pagination import *
from .filters import *

# Create your views here.

class EmpruntViewSet(viewsets.ModelViewSet):
    """
        ViewSet that manages Emprunt with CRUD methods
    """

    queryset = Emprunt.objects.all()
    serializer_class = EmpruntSerializer
    permission_classes = [
        IsAdminOrMembreToBookOrShareOpinion,
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrEmpruntBelongsToMember,    
    ]
    pagination_class = EmpruntPagination
    filterset_class = EmpruntFilterSet
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]   
    ordering_fields = ['date_ret', 'retourne', 'date_emp']

    def list(self, request, membres_pk=None, livres_pk=None):

        cache_key = 'emprunts-list-%s-%s' % (membres_pk, livres_pk)
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

        if request.user.is_staff:      
            if livres_pk:
                emprunts = self.paginate_queryset(self.filter_queryset(self.get_queryset().filter(livre=livres_pk)))
            elif membres_pk:
                emprunts = self.paginate_queryset(self.filter_queryset(self.get_queryset().filter(membre=membres_pk)))
            else:    
                emprunts = self.paginate_queryset(self.filter_queryset(self.get_queryset()))
        else: 
            try:
                emprunts = self.paginate_queryset(self.filter_queryset(self.get_queryset().filter(membre=request.user.membre)))
            except:
                emprunts = None

        serializer = EmpruntSerializer(emprunts, many=True)
        cache.set(cache_key, [self.paginator.page, serializer.data], cache_time)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk, membres_pk=None, livres_pk=None):
        cache_key = 'emprunts-%s-%s-%s' % (pk, membres_pk, livres_pk)
        cache_time = 86400 # time in seconds for cache to be valid
        #cache.set(cache_key, None, cache_time)   
        data = cache.get(cache_key) # returns None if no key-value pair   

        if not data:
            emprunt = self.queryset.get(pk=pk)
            serializer = EmpruntSerializer(emprunt)
            cache.set(cache_key, serializer.data, cache_time)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(data, status=status.HTTP_200_OK)

    @extend_schema(
        description='Method that sets a Membre to an Emprunt',
        examples=[
            OpenApiExample(
                'Example 1',
                description='method put on /emprunts/1/set-membre/1/',
                value="{'status': 'membre added'}"
            ),
        ],
    )
    @action(detail=True, methods=['patch', 'put'], url_path='set-membre/(?P<membre_pk>\d+)')
    def set_membre(self, request, pk=None, membre_pk=None):
        emprunt = self.get_object()
        membre = get_object_or_404(Membre, pk=membre_pk)
        emprunt.membre = membre
        emprunt.full_clean()
        emprunt.save()
        return Response({'status': 'membre added'}, status=status.HTTP_204_NO_CONTENT)
    
    @extend_schema(
        description='Method that removes a Membre from an Emprunt',
        examples=[
            OpenApiExample(
                'Example 1',
                description='method put on /emprunts/1/remove-membre/1/',
                value="{'status': 'membre removed'}"
            ),
        ],
    )
    @action(detail=True, methods=['patch', 'put'], url_path='remove-membre/(?P<membre_pk>\d+)')
    def remove_membre(self, request, pk=None, membre_pk=None):
        emprunt = self.get_object()
        if emprunt.membre :
            emprunt.membre = None
            emprunt.full_clean()
            emprunt.save()
            return Response({'status': 'membre removed'}, status=status.HTTP_204_NO_CONTENT)
    
        return Response({'status': 'this emprunt has no membre'}, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        description='Method that sets a Livre to an Emprunt',
        examples=[
            OpenApiExample(
                'Example 1',
                description='method put on /emprunts/1/set-livre/1/',
                value="{'status': 'livre added'}"
            ),
        ],
    )
    @action(detail=True, methods=['patch', 'put'], url_path='set-livre/(?P<livre_pk>\d+)')
    def set_livre(self, request, pk=None, livre_pk=None):
        emprunt = self.get_object()
        livre = get_object_or_404(Livre, pk=livre_pk)
        emprunt.livre = livre
        emprunt.full_clean()
        emprunt.save()
        return Response({'status': 'livre added'}, status=status.HTTP_204_NO_CONTENT)
    
    @extend_schema(
        description='Method that removes a Livre from an Emprunt',
        examples=[
            OpenApiExample(
                'Example 1',
                description='method put on /emprunts/1/remove-livre/1/',
                value="{'status': 'livre removed'}"
            ),
        ],
    )
    @action(detail=True, methods=['patch', 'put'], url_path='remove-livre/(?P<livre_pk>\d+)')
    def remove_livre(self, request, pk=None, livre_pk=None):
        emprunt = self.get_object()
        if emprunt.livre :
            emprunt.livre = None
            emprunt.full_clean()
            emprunt.save()
            return Response({'status': 'livre removed'}, status=status.HTTP_204_NO_CONTENT)
    
        return Response({'status': 'this emprunt has no livre'}, status=status.HTTP_400_BAD_REQUEST)
    

class MembreViewSet(viewsets.ModelViewSet):
    """
        ViewSet that manages Membres with CRUD methods
    """
    queryset = Membre.objects.all()
    serializer_class = MembreSerializer
    permission_classes = [
        permissions.IsAdminUser,
    ]
    pagination_class = MembrePagination
    filterset_class = MembreFilterSet
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]   
    ordering_fields = ['user__first_name', 'user__last_name']

    @extend_schema(
        description='Method that adds an Emprunt to a Membre',
        examples=[
            OpenApiExample(
                'Example 1',
                description='method put on /membres/1/add-emprunt/1/',
                value="{'status': 'emprunt added'}"
            ),
        ],
    )
    @action(detail=True, methods=['patch', 'put'], url_path='add-emprunt/(?P<emprunt_pk>\d+)')
    def set_membre(self, request, pk=None, emprunt_pk=None):
        membre = self.get_object()
        emprunt = get_object_or_404(Emprunt, pk=emprunt_pk)

        if emprunt.membre:
            return Response({'status': 'this emprunt is already related to a Membre'}, status=status.HTTP_400_BAD_REQUEST)
        
        membre.emprunt_set.add(emprunt)
        membre.full_clean()
        membre.save()
        return Response({'status': 'membre added'}, status=status.HTTP_204_NO_CONTENT)
    
    @extend_schema(
        description='Method that remove an Emprunt from a Membre',
        examples=[
            OpenApiExample(
                'Example 1',
                description='method put on /membres/1/remove-emprunt/1/',
                value="{'status': 'emprunt removed'}"
            ),
        ],
    )
    @action(detail=True, methods=['patch', 'put'], url_path='remove-emprunt/(?P<emprunt_pk>\d+)')
    def remove_membre(self, request, pk=None, emprunt_pk=None):
        membre = self.get_object()
        emprunt = get_object_or_404(Emprunt, pk=emprunt_pk)
        membre.emprunt_set.remove(emprunt) 
        membre.full_clean()
        membre.save()
        return Response({'status': 'membre removed'}, status=status.HTTP_204_NO_CONTENT)
    
    @extend_schema(
        description='Method that adds an Avis to a Membre',
        examples=[
            OpenApiExample(
                'Example 1',
                description='method put on /membres/1/add-avis/1/',
                value="{'status': 'avis added'}"
            ),
        ],
    )
    @action(detail=True, methods=['patch', 'put'], url_path='add-avis/(?P<avis_pk>\d+)')
    def set_avis(self, request, pk=None, avis_pk=None):
        membre = self.get_object()
        avis = get_object_or_404(Avis, pk=avis_pk)

        if avis.membre:
            return Response({'status': 'this Avis is already related to a Membre'}, status=status.HTTP_400_BAD_REQUEST)
        
        membre.avis_set.add(avis)
        membre.full_clean()
        membre.save()
        return Response({'status': 'avis added'}, status=status.HTTP_204_NO_CONTENT)
    
    @extend_schema(
        description='Method that remove an Avis from a Membre',
        examples=[
            OpenApiExample(
                'Example 1',
                description='method put on /membres/1/remove-avis/1/',
                value="{'status': 'avis removed'}"
            ),
        ],
    )
    @action(detail=True, methods=['patch', 'put'], url_path='remove-avis/(?P<avis_pk>\d+)')
    def remove_avis(self, request, pk=None, avis_pk=None):
        membre = self.get_object()
        avis = get_object_or_404(Avis, pk=avis_pk)
        membre.avis_set.remove(avis)
        membre.full_clean()
        membre.save()
        return Response({'status': 'avis removed'}, status=status.HTTP_204_NO_CONTENT)
  

class AvisViewSet(viewsets.ModelViewSet):
    """
        ViewSet that manages Avis with CRUD methods
    """
    
    queryset = Avis.objects.all()
    serializer_class = AvisSerializer
    permission_classes = [
        IsAdminOrMembreToBookOrShareOpinion, 
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrAvisBelongsToMember,
    ]   
    pagination_class = AvisPagination
    filterset_class = AvisFilterSet
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]   
    ordering_fields = ['note', 'livre__titre']

    def list(self, request, membres_pk=None, livres_pk=None):

        if livres_pk:
            avis = self.paginate_queryset(self.filter_queryset(self.get_queryset().filter(livre=livres_pk)))
        elif membres_pk:
            avis = self.paginate_queryset(self.filter_queryset(self.get_queryset().filter(membre=membres_pk)))
        else:
            if request.user.is_staff:      
                avis = self.paginate_queryset(self.filter_queryset(self.get_queryset()))
            else: 
                try:
                    avis = self.paginate_queryset(self.filter_queryset(self.get_queryset().filter(membre=request.user.membre)))
                except:
                    avis = None

        serializer = AvisSerializer(avis, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @extend_schema(
        description='Method that sets a Membre to an Avis',
        examples=[
            OpenApiExample(
                'Example 1',
                description='method put on /avis/1/set-membre/1/',
                value="{'status': 'membre added'}"
            ),
        ],
    )
    @action(detail=True, methods=['patch', 'put'], url_path='set-membre/(?P<membre_pk>\d+)')
    def set_membre(self, request, pk=None, membre_pk=None):
        avis = self.get_object()
        membre = get_object_or_404(Membre, pk=membre_pk)
        avis.membre = membre
        avis.full_clean()
        avis.save()
        return Response({'status': 'membre added'}, status=status.HTTP_204_NO_CONTENT)
    
    @extend_schema(
        description='Method that removes a Membre from an Avis',
        examples=[
            OpenApiExample(
                'Example 1',
                description='method put on /avis/1/remove-membre/1/',
                value="{'status': 'membre removed'}"
            ),
        ],
    )
    @action(detail=True, methods=['patch', 'put'], url_path='remove-membre/(?P<membre_pk>\d+)')
    def remove_membre(self, request, pk=None, membre_pk=None):
        avis = self.get_object()
        if avis.membre :
            avis.membre = None
            avis.full_clean()
            avis.save()
            return Response({'status': 'livre removed'}, status=status.HTTP_204_NO_CONTENT)
    
        return Response({'status': 'this avis has no membre'}, status=status.HTTP_400_BAD_REQUEST)
    
    
    @extend_schema(
        description='Method that sets a Livre to an Avis',
        examples=[
            OpenApiExample(
                'Example 1',
                description='method put on /avis/1/set-livre/1/',
                value="{'status': 'livre added'}"
            ),
        ],
    )

    @action(detail=True, methods=['patch', 'put'], url_path='set-livre/(?P<livre_pk>\d+)')
    def set_livre(self, request, pk=None, livre_pk=None):
        avis = self.get_object()
        livre = get_object_or_404(Livre, pk=livre_pk)
        avis.livre = livre
        avis.full_clean()
        avis.save()
        return Response({'status': 'livre added'}, status=status.HTTP_204_NO_CONTENT)
    
    @extend_schema(
        description='Method that removes a Livre from an Avis',
        examples=[
            OpenApiExample(
                'Example 1',
                description='method put on /avis/1/remove-livre/1/',
                value="{'status': 'livre removed'}"
            ),
        ],
    )
    @action(detail=True, methods=['patch', 'put'], url_path='remove-livre/(?P<livre_pk>\d+)')
    def remove_livre(self, request, pk=None, livre_pk=None):
        avis = self.get_object()
        if avis.livre :
            avis.livre= None
            avis.full_clean()
            avis.save()
            return Response({'status': 'livre removed'}, status=status.HTTP_204_NO_CONTENT)
    
        return Response({'status': 'this avis has no livre'}, status=status.HTTP_400_BAD_REQUEST)
    