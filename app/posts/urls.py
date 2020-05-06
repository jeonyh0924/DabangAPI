from django.urls import path, include
from rest_framework.routers import DefaultRouter

from posts import apis
from posts.apis import getBorodCityList, getEupMyunDongList, getSiGunGuList, BrokerAPIView

urlpatterns_posts = [
    # 포스트 CRUD URLS
    path('test/', apis.PostTinytList.as_view()),
    # 포스트 서브 CRUD URLS
    path('broker/', BrokerAPIView.as_view()),
    path('postLike/', apis.PostLikeView.as_view()),

    # 기타 URLS
    path('bjd/', apis.getAptListService),
    path('bc/', getBorodCityList),
    path('sg/', getSiGunGuList),
    path('emd/', getEupMyunDongList),
]

router = DefaultRouter()
router.register('complex', apis.ComplexViewSet)
router.register('address', apis.AddressViewSet)
router.register('salesForm', apis.SalesFormViewSet)
router.register('maintenance', apis.MaintenanceFeeViewSet)
router.register('ss', apis.SecuritySafetyViewSet)
router.register('post', apis.PostRoomViewSet)
urlpatterns_posts += [
    path('', include(router.urls))
]
