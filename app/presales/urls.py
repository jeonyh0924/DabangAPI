from django.urls import path, include
from rest_framework.routers import DefaultRouter

from presales import apis
from presales.apis import getPreSaleTinyAPIView

router = DefaultRouter()
router.register('', apis.PreSaleViewSet)
urlpatterns_presales = [
    path('tiny/', getPreSaleTinyAPIView),
]
urlpatterns_presales += [
    path('', include(router.urls)),
]
