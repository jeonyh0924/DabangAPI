from django.urls import path, include
from rest_framework.routers import DefaultRouter

from presales import apis
from presales.apis import getPreSaleTinyAPIView, themaFilterAPIView, brandFilterAPIView

router = DefaultRouter()
router.register('', apis.PreSaleViewSet)
urlpatterns_presales = [
    path('tiny/', getPreSaleTinyAPIView),
    path('thema/', themaFilterAPIView),
    path('brand/', brandFilterAPIView),
]
urlpatterns_presales += [
    path('', include(router.urls)),
]
