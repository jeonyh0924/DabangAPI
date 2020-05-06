from django.urls import path, include
from rest_framework.routers import DefaultRouter

from posts import apis
from posts.apis import getBorodCityList, getEupMyunDongList, getSiGunGuList, BrokerAPIView

urlpatterns_posts = [
    # 포스트 CRUD URLS
    path('test/', apis.PostTinytList.as_view()),
    path('list/', apis.PostList.as_view()),
    path('', apis.PostDetail.as_view()),

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

urlpatterns_posts += [
    path('', include(router.urls))
]
