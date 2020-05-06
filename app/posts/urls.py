from django.urls import path
from posts import apis
from posts.apis import getBorodCityList, getEupMyunDongList, getSiGunGuList, ComplexAPIView, ComplexDetail

urlpatterns_posts = [
    path('test/', apis.PostTestList.as_view()),
    path('list/', apis.PostList.as_view()),
    path('', apis.PostDetail.as_view()),
    path('postLike/', apis.PostLikeView.as_view()),

    path('complexDetail/', ComplexDetail),
    path('complex/', ComplexAPIView),
    path('bjd/', apis.getAptListService),
    path('bc/', getBorodCityList),
    path('sg/', getSiGunGuList),
    path('emd/', getEupMyunDongList),
]
