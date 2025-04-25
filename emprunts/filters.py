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
        

    