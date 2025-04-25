from django.shortcuts import render,get_object_or_404
from rest_framework import filters, viewsets, status
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
    permission_classes = [IsAdminOrMembre]
    pagination_class = EmpruntPagination
    filterset_class = EmpruntFilterSet
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]   
    ordering_fields = ['date_ret', 'retourne', 'date_emp']

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
        membre = get_object_or_404(Membre, pk=membre_pk)
        emprunt.membre = None
        emprunt.full_clean()
        emprunt.save()
        return Response({'status': 'membre removed'}, status=status.HTTP_204_NO_CONTENT)
    
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
        livre = get_object_or_404(Livre, pk=livre_pk)
        emprunt.livre = None
        emprunt.full_clean()
        emprunt.save()
        return Response({'status': 'livre removed'}, status=status.HTTP_204_NO_CONTENT)
    
    

class MembreViewSet(viewsets.ModelViewSet):
    
    queryset = Membre.objects.all()
    serializer_class = MembreSerializer
    #permission_classes = [IsAdminOrMembre]
    #pagination_class = EmpruntPagination
    #ordering_fields = ['user__last_name', 'user__first_name']

class AvisViewSet(viewsets.ModelViewSet):
    
    queryset = Avis.objects.all()
    serializer_class = AvisSerializer
    #permission_classes = [IsAdminOrMembre]
    #pagination_class = EmpruntPagination
    #ordering_fields = ['user__last_name', 'user__first_name']