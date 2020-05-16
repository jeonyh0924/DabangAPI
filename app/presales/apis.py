from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from presales.models import PreSale, Thema, Brand
from presales.serializer import PreSaleSerializer, PreSaleTinySerializer
from django_filters.rest_framework import DjangoFilterBackend


class PreSaleViewSet(ModelViewSet):
    queryset = PreSale.objects.all()
    serializer_class = PreSaleSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['brand', 'thema']
    search_fields = ['brand', 'thema']


@api_view()
def getPreSaleTinyAPIView(request):
    queryset = PreSale.objects.all()
    serilaizer = PreSaleTinySerializer(queryset, many=True, )
    return Response(serilaizer.data, status=status.HTTP_200_OK)


@api_view()
def themaFilterAPIView(request):
    thema = request.query_params.get('thema')
    thema = get_object_or_404(Thema, name=thema)
    thema = thema.pk
    pre = PreSale.objects.filter(thema=thema)
    serializer = PreSaleTinySerializer(pre, many=True, )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view()
def brandFilterAPIView(request):
    brand = request.query_params.get('brand')
    brand = get_object_or_404(Brand, name=brand)
    brand = brand.pk
    pre = PreSale.objects.filter(brand=brand)
    serializer = PreSaleTinySerializer(pre, many=True, )
    return Response(serializer.data, status=status.HTTP_200_OK)