import django_filters
from django_filters.widgets import RangeWidget
from .models import *

class EmpruntFilterSet(django_filters.FilterSet):
    livre__titre = django_filters.CharFilter(lookup_expr='icontains', field_name='livre__titre')
    
    date_emp = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={'type': 'date'}))
    date_ret = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={'type': 'date'}))
    retourne = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={'type': 'date'}))
    
    class Meta:
        model = Emprunt
        fields = [
            'livre__titre',
            'date_emp',
            'date_ret',
            'retourne',
            'membre__user__first_name',
            'membre__user__last_name'
        ]

class AvisFilterSet(django_filters.FilterSet):
    commentaire = django_filters.CharFilter(lookup_expr='icontains', field_name='commentaire')
    livre__titre = django_filters.CharFilter(lookup_expr='icontains', field_name='livre__titre')
    
    class Meta:
        model = Avis
        fields = [
            'note',
            'commentaire',
            'livre__titre',
            'membre'
        ]
        
class MembreFilterSet(django_filters.FilterSet):
    adresse = django_filters.CharFilter(lookup_expr='icontains', field_name='adresse')
    
    class Meta:
        model = Membre
        fields = [
            'user__first_name',
            'user__last_name',
            'adresse',
            'telephone',
        ]
    