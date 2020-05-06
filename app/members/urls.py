from django.urls import path, include
from rest_framework.routers import DefaultRouter

from members import views
from members.apis import getRecentlyPostListView, getContactToBroker
from . import apis

# from members.apis import socialLogin


router = DefaultRouter()
router.register('', apis.UserModelViewSet)

urlpatterns_members = [
    # path('socialLogin/', socialLogin.as_view()),
    path('kakaoToken/', apis.KakaoJwtTokenView.as_view()),
    path('facebookToken/', apis.FacebookJwtToken.as_view()),
    path('kakao-login/', views.kakao_login),
    path('recently/', getRecentlyPostListView),
    path('contactTo/', getContactToBroker),

]
urlpatterns_members += router.urls
