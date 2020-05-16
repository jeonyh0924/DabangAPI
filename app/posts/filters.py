from django.db.models import Q
from django_filters import rest_framework as filters

from posts.models import PostRoom


class PostFilter(filters.FilterSet):
    type = filters.CharFilter(method='filter_types')
    salesForm__type = filters.CharFilter(method='salesForm__types')
    floor = filters.CharFilter(method='filter_floor')

    parkingTF = filters.BooleanFilter()
    pet = filters.BooleanFilter()
    shortRent = filters.BooleanFilter()
    elevator = filters.BooleanFilter()
    builtIn = filters.BooleanFilter()
    veranda = filters.BooleanFilter()
    depositLoan = filters.BooleanFilter()

    # 방크기
    min_supply_area = filters.NumberFilter(field_name='supplyAreaInt', lookup_expr='gte')
    max_supply_area = filters.NumberFilter(field_name='supplyAreaInt', lookup_expr='lte')

    # 보증금/전세가
    min_depositInt = filters.NumberFilter(field_name='salesForm__depositInt', lookup_expr='gte')
    max_depositInt = filters.NumberFilter(field_name='salesForm__depositInt', lookup_expr='lte')

    # 월세
    min_monthlyInt = filters.NumberFilter(field_name='salesForm__monthlyInt', lookup_expr='gte')
    max_monthlyInt = filters.NumberFilter(field_name='salesForm__monthlyInt', lookup_expr='lte')

    class Meta:
        models = PostRoom
        fields = [
            'type',
            'salesForm__type',
            'complete',
            'min_supply_area',
            'max_supply_area',
            'min_depositInt',
            'max_depositInt',
            'min_monthlyInt',
            'max_monthlyInt'

        ]

    def filter_types(self, queryset, name, value):
        filter_object = Q()
        for type in value.split(','):
            filter_object |= Q(type=type)
        return queryset.filter(filter_object)

    def salesForm__types(self, queryset, name, value):
        filter_object = Q()
        for type in value.split(','):
            filter_object |= Q(salesForm__type=type)
        return queryset.filter(filter_object)

    def filter_floor(self, queryset, name, value):
        filter_object = Q()
        for floor in value.split(','):
            filter_object |= Q(floor=floor)
        return queryset.filter(filter_object)
