import json

import requests
from django.contrib.auth import get_user_model

from django.contrib.auth.models import User

from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view

from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

from members.models import SocialLogin, RecentlyPostList, ContactToBroker, RecentlyComplexLis
from members.permissions import IsProfileOwnerOrReadOnly
from members.serializers import UserSerializer, UserProfileSerializer, UserPostLikePostSerializer, UserPostSerializer, \
    UserComplexsSerializer, UserComplexLikeSerializer, UserBrokerSerializer
from posts.models import PostRoom, Broker, ComplexInformation
from posts.serializers import PostTinySerializer, PostListSerializer

User = get_user_model()
JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class UserModelViewSet(viewsets.ModelViewSet):
    """
    viewsets.ModelViewSet 특징
    'list', 'create', 'retrieve', 'update', 'destroy' 기능 자동 지원, 별도의 함수 작성 가능 api코드 간소화

    # 함수들을 오버라이딩 하는 경우 상속받는 기능의 코드를 이해한 상태에서 건드려야 생산성과 유지보수의 이점을 둘 다 가져가는 듯 하다.
    # 각 함수를 오버라이딩 할 때 어떤 모듈의 함수인지 이해하는 지식 필요할 듯

    추후 추가할 기능들
     - 유저 프로필 페이지 최근 본 게시글 목록, 찜한 게시글 목록
     - 회원가입 시 유저 아이디 중복 체크
     - 유저 패스워드 변경
     - 특정 상황에 따른 푸쉬알림
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save()

    def get_serializer_class(self):
        if self.action in "create":
            serializer_class = UserSerializer
            return serializer_class
        else:
            serializer_class = UserProfileSerializer
            return serializer_class

    def get_permissions(self):
        if self.action == ("partial_update", "update", "destroy"):
            permission_classes = [IsProfileOwnerOrReadOnly()]
            return permission_classes
        elif self.action == ("retrieve", "partial_update", "update", "destroy"):
            permission_classes = [IsAuthenticated()]
            return permission_classes
        elif self.action == "list":
            # 모든 유저의 목록을 보여주고 싶지 않아서
            permission_classes = [IsAdminUser()]
            return permission_classes
        else:
            permission_classes = [AllowAny()]
            return permission_classes

    @action(detail=False, methods=['POST'])
    def jwt(self, request):
        email = request.data.get('email')
        if not User.objects.filter(email=email).exists():
            data = {
                'message': ' 유저의 이메일 정보가 올바르지 않습니다.'
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        password = request.data.get('password')
        user = User.objects.get(email=email)
        if user.check_password(password):
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            # user = authenticate(username=username, password=userpass)
            data = {
                'token': jwt_token,
                'user': UserSerializer(user).data
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {
                'message': '정보가 올바르지 않습니다.'
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'])
    def postlike(self, request):
        user = request.user
        posts = PostRoom.objects.filter(postlikes__user=user)
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def recentlyPosts(self, request):
        user = request.user
        serializer = UserPostSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def complexs(self, request):
        user = request.user
        serializer = UserComplexsSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def complike(self, request):
        user = request.user
        serializer = UserComplexLikeSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def brokers(self, request):
        user = request.user
        serializer = UserBrokerSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def posts(self, request):
        user = request.user
        posts = user.postroom_set.all()
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class KakaoJwtTokenView(APIView):
    def post(self, request):
        access_token = request.data.get('accessToken')
        url = 'https://kapi.kakao.com/v2/user/me'
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
        }
        kakao_response = requests.post(url, headers=headers)

        user_data = kakao_response.json()
        kakao_id = user_data['id']
        user_username = user_data['properties']['nickname']
        user_first_name = user_username[1:]
        user_last_name = user_username[0]
        try:
            user = User.objects.get(username=kakao_id)
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=kakao_id,
                email=f'{kakao_id}@daum.net'
            )
        payload = JWT_PAYLOAD_HANDLER(user)
        jwt_token = JWT_ENCODE_HANDLER(payload)

        kakao = SocialLogin.objects.filter(type='kakao')[0]

        user.social.add(kakao)
        data = {
            'token': jwt_token,
            'user': UserSerializer(user).data,
        }

        return Response(data)


class FacebookJwtToken(APIView):
    api_base = 'https://graph.facebook.com/v3.2'
    api_get_access_token = f'{api_base}/oauth/access_token'
    api_me = f'{api_base}/me'

    def post(self, request):
        access_token = request.data.get('accessToken')
        params = {
            'access_token': access_token,
            'fields': ','.join([
                'id',
                'first_name',
                'last_name',
                'picture.type(large)',
            ])
        }
        response = requests.get(self.api_me, params)
        data = response.json()

        facebook_id = data['id']
        first_name = data['first_name']
        last_name = data['last_name']

        try:
            user = User.objects.get(username=facebook_id)
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=facebook_id,
                email=f'{facebook_id}@facebook.com'
            )
        payload = JWT_PAYLOAD_HANDLER(user)
        jwt_token = JWT_ENCODE_HANDLER(payload)
        facebook = SocialLogin.objects.filter(type='facebook')[0]
        user.social.add(facebook)
        data = {
            'token': jwt_token,
            'user': UserSerializer(user).data,
        }
        return Response(data)


@api_view()
def getRecentlyPostListView(request):
    post = request.data.get('post')

    post = int(post)
    post = PostRoom.objects.get(pk=post)
    dump = RecentlyPostList.objects.filter(user=request.user, post=post)
    data = {
        'message': f"{post}번 방은 이미 최신글 리스트에 존재하는 게시글 입니다."
    }
    if dump:
        return Response(
            data, status=status.HTTP_400_BAD_REQUEST
        )
    # while True:
    #     social_user = RecentlyPostList.objects.filter(user=request.user.pk)
    #     user_post_count = len(social_user)
    #
    #     if user_post_count >= 5:
    #         social_user[0].delete()
    #     else:
    #         break
    RecentlyPostList.objects.get_or_create(
        user=request.user,
        post=post,
    )
    data = {
        "message": f"{post} 번 방이 최근 유저 정보 리스트에 추가되었습니다."
    }
    return Response(data, status=status.HTTP_200_OK)


@api_view()
def getRecentlyComplexListView(request):
    complex_pk = request.data.get('complex_ins')

    copmlex_pk = int(complex_pk)
    complex_ins = ComplexInformation.objects.get(pk=complex_pk)

    if RecentlyComplexLis.objects.filter(user=request.user, complex_ins=complex_ins).exists():
        data = {
            'message': f"{complex_pk}번 단지는 이미 최신글 리스트에 존재하는 게시글 입니다."
        }
        return Response(
            data, status=status.HTTP_400_BAD_REQUEST
        )
    RecentlyComplexLis.objects.get_or_create(
        user=request.user,
        complex_ins=complex_ins
    )
    data = {
        "message": f"{complex_pk} 번 단지가 최근 유저 정보 리스트에 추가되었습니다."
    }
    return Response(data, status=status.HTTP_200_OK)


@api_view()
def getContactToBroker(request):
    broker = request.data.get('broker')
    broker = int(broker)
    broker = Broker.objects.get(pk=broker)
    record = ContactToBroker.objects.filter(user=request.user, broker=broker)
    if record:
        data = {
            'message': '이미 연락했던 부동산 입니다.'
        }
        user_list = ContactToBroker.objects.filter(user=request.user.pk)
        print(user_list)
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    while True:
        user_list = ContactToBroker.objects.filter(user=request.user.pk)
        user_count_list = len(user_list)

        if user_count_list >= 5:
            user_list[0].delete()
        else:
            break

    ContactToBroker.objects.get_or_create(
        user=request.user,
        broker=broker,
    )
    data = {
        "message": "연락한 부동산 리스트에 추가되었습니다."
    }
    user_list = ContactToBroker.objects.filter(user=request.user.pk)
    print(user_list)
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def AppleSocialLogin(request):
    email = request.data.get('email')
    username = request.data.get('username')
    social = request.data.get('social')
    if not social:
        data = {
            'message': '소셜 타입을 명시하세요.'
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    if social == 'apple':
        apple_ins = SocialLogin.objects.get(type=social)
        user, __ = User.objects.get_or_create(email=email, username=username)
        user.social.add(apple_ins)
        payload = JWT_PAYLOAD_HANDLER(user)
        jwt_token = JWT_ENCODE_HANDLER(payload)
        data = {
            'token': jwt_token,
            'user': UserSerializer(user).data
        }
        return Response(data, status=status.HTTP_200_OK)
    data = {
        'message': 'apple 로그인을 위한 요청 주소입니다.'
    }
    return Response(data, status=status.HTTP_400_BAD_REQUEST)
