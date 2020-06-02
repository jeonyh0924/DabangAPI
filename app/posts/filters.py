from django.db.models import Q
from django_filters import rest_framework as filters

from posts.models import PostRoom


class PostFilter(filters.FilterSet):
    """
    filter를 정의하는 경우, 주요한 2개의 argument
    name = "" 모델 필드의 이름을 필터링 한다.
    lookup_expr="" loopup_expr 조건문을 사용하여 조회 필드를 정의한다. 장고에서 구문은

    """
    type = filters.CharFilter(method='filter_types')
    salesForm__type = filters.CharFilter(method='salesForm__types')
    floor = filters.CharFilter(method='filter_floor')

    # 위도 경도
    # lng = filters.NumericRangeFilter(method='filter_lng')
    lng = filters.CharFilter(method='filter_lng')
    lat = filters.CharFilter(method='filter_lat')

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
            # 'lng',
            # 'lat',
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

    def filter_lng(self, queryset, name, value):
        """
        여기서, distance를 다른 변수로 받은다음 사용을 할 수 있는지가 궁금합니다.
        """
        lng, distance = map(float, value.split(','))
        variable_for_lng = 0.009197
        boundary = {
            "max_lng": lng + variable_for_lng * distance,
            "min_lng": lng - variable_for_lng * distance,
        }
        filter_object = Q(lng__gte=boundary['min_lng']) & Q(lng__lte=boundary['max_lng'])
        return queryset.filter(filter_object)

    def filter_lat(self, queryset, name, value):
        lat, distance = map(float, value.split(','))
        variable_for_lat = 0.0083

        boundary = {
            "max_lat": lat + variable_for_lat * distance,
            "min_lat": lat - variable_for_lat * distance,
        }
        filter_object = Q(lat__gte=boundary['min_lat']) & Q(lat__lte=boundary['max_lat'])
        return queryset.filter(filter_object)
