import django_filters
from rest_framework import filters

from django_filters.filterset import FilterSet

from .models import Log

class LogFilter(FilterSet):
    timestamp_gte = django_filters.IsoDateTimeFilter(field_name='created_at',lookup_expr='gte')
    
    class Meta:
        model = Log
        fields = ['timestamp_gte']
    