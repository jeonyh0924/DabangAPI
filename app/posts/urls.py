from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from posts import apis
from posts.apis import getBorodCityList, getEupMyunDongList, getSiGunGuList, ComplexAPIView, ComplexDetail
from posts import apis, views
from posts.apis import getBorodCityList, getEupMyunDongList, getSiGunGuList

urlpatterns_posts = [
    path('list/', apis.PostList.as_view()),
    path('', apis.PostDetail.as_view()),

    path('create/', apis.PostCreateView.as_view()),
    path('imageupload/', apis.ImageUploadView.as_view()),

    path('postLike/', apis.PostLikeView.as_view()),

    path('image/', apis.PostImageView.as_view()),
    # path('deberg-test/', views.deberg_test),
    # path('postFiltering/', apis.PostFiltering.as_view()),

    # 전영훈 urls -----
    path('complexDetail/', ComplexDetail),
    path('complex/', ComplexAPIView),
    path('bjd/', apis.getAptListService),
    path('bc/', getBorodCityList),
    path('sg/', getSiGunGuList),
    path('emd/', getEupMyunDongList),
]
