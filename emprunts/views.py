from django.shortcuts import render,get_object_or_404
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

    def list(self, request, membres_pk=None):
        if request.user.is_staff:      
            emprunts = self.paginate_queryset(self.filter_queryset(self.get_queryset()))
        else: 
            try:
                emprunts = self.paginate_queryset(self.filter_queryset(self.get_queryset().filter(membre=request.user.membre)))
            except:
                emprunts = self.paginate_queryset(self.filter_queryset(self.get_queryset().filter(membre=None)))   

        serializer = EmpruntSerializer(emprunts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
    
    queryset = Membre.objects.all()
    serializer_class = MembreSerializer
    #permission_classes = [IsAdminOrMembre]
    #pagination_class = EmpruntPagination
    #ordering_fields = ['user__last_name', 'user__first_name']

class AvisViewSet(viewsets.ModelViewSet):
    
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

    def list(self, request, membres_pk=None):
        if request.user.is_staff or membres_pk:      
            avis = self.paginate_queryset(self.filter_queryset(self.get_queryset()))
        else: 
            try:
                avis = self.paginate_queryset(self.filter_queryset(self.get_queryset().filter(membre=request.user.membre)))
            except:
                avis = self.paginate_queryset(self.filter_queryset(self.get_queryset().filter(membre=None)))   

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
    