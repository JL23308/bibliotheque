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

# Create your views here.

class EmpruntViewSet(viewsets.ModelViewSet):
    
    queryset = Emprunt.objects.all()
    serializer_class = EmpruntSerializer
    permission_classes = [IsAdminOrMembre]
    pagination_class = EmpruntPagination
    #ordering_fields = ['user__last_name', 'user__first_name']

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
        return Response({'status': 'membre added'}, status=status.HTTP_200_OK)
    
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
    @action(detail=True, methods=['patch', 'put'], url_path='set-livre/(?P<membre_pk>\d+)')
    def set_livre(self, request, pk=None, livre_pk=None):
        emprunt = self.get_object()
        livre = get_object_or_404(Livre, pk=livre_pk)
        emprunt.livre = livre
        emprunt.full_clean()
        emprunt.save()
        return Response({'status': 'livre added'}, status=status.HTTP_200_OK)
    

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