import django_filters
from django_filters.widgets import RangeWidget
from .models import *

class LivreFilterSet(django_filters.FilterSet):
    titre = django_filters.CharFilter(lookup_expr='icontains', field_name='titre')
    date_publication = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={'type': 'date'}))
    
    class Meta:
        model = Livre
        fields = [
            'titre', 
            'auteur__nom', 
            'auteur__prenom',
            'date_publication',
            'categorie__nom',
            ]
        
class CategorieFilterSet(django_filters.FilterSet):
    class Meta:
        model = Categorie
        fields = ['nom']
        
class AuteurFilterSet(django_filters.FilterSet):
    date_naissance = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={'type': 'date'}))

    class Meta:
        model = Auteur
        fields = [
            'nom', 
            'prenom',
            ]
        

    