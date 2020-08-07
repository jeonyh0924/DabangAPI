from django.urls import path, include
from rest_framework.routers import DefaultRouter

from posts import apis, views
from posts.apis import getBorodCityList, getEupMyunDongList, getSiGunGuList, BrokerAPIView, PostDivisionFilter

urlpatterns_posts = [
    #  방 생성 uls
    # path('create/', apis.PostCreateAPIVie.as_view()),

    # 포스트 CRUD URLS
    path('tiny/', apis.PostTinytList.as_view()),
    # 포스트 서브 CRUD URLS
    path('broker/', BrokerAPIView.as_view()),
    path('postLike/', apis.PostLikeView.as_view()),
    path('compLike/', apis.ComplexLikeView.as_view()),

    # 기타 URLS
    path('bjd/', apis.getAptListService),
    path('bc/', getBorodCityList),
    path('sg/', getSiGunGuList),
    path('emd/', getEupMyunDongList),

    # 방 위도 경도 필터링
    path('distance/', PostDivisionFilter),
    path('complex/<int:pk>/', apis.ComplexDetailAPIView.as_view()),

]

router = DefaultRouter()
# router.register('complex', apis.ComplexViewSet)
router.register('address', apis.AddressViewSet)
router.register('salesForm', apis.SalesFormViewSet)
router.register('maintenance', apis.MaintenanceFeeViewSet)
router.register('ss', apis.SecuritySafetyViewSet)
router.register('', apis.PostRoomViewSet)
urlpatterns_posts += [
    path('', include(router.urls))
]
