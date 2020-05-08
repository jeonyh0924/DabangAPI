from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from presales.models import PreSale
from presales.serializer import PreSaleSerializer, PreSaleTinySerializer


class PreSaleViewSet(ModelViewSet):
    queryset = PreSale.objects.all()
    serializer_class = PreSaleSerializer


@api_view()
def getPreSaleTinyAPIView(request):
    queryset = PreSale.objects.all()
    serilaizer = PreSaleTinySerializer(queryset, many=True, )
    # if serilaizer.is_valid():
    return Response(serilaizer.data, status=status.HTTP_200_OK)
    # return Response(serilaizer.errors, status=status.HTTP_400_BAD_REQUEST)
