import json
import os
import urllib
from django.core.files import File
import requests
import xmltodict
from django.http import Http404
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException
from rest_framework.generics import RetrieveAPIView, get_object_or_404
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from config.settings.base import MEDIA_ROOT
from posts.models import PostLike, Broker, PostAddress, SalesForm, MaintenanceFee, SecuritySafetyFacilities, PostImage, \
    AdministrativeDetail, OptionItem, RoomOption, RoomSecurity
from posts.models import PostRoom, ComplexInformation
from posts.permissions import IsOwnerOrReadOnly
from posts.serializers import PostLikeSerializer, PostTinySerializer, BrokerSerializer, AddressSerializer, \
    SalesFormSerializer, ManagementSerializer, SecuritySafetySerializer, PostCreateSerializer
from posts.serializers import PostListSerializer, ComplexInformationSerializer

secret = 'V8giduxGZ%2BU463maB552xw3jULhTVPrv%2B7m2qSqu4w8el9fk8bnMD9i6rjUQz7gcUcFnDKyOmcCBztcbVx3Ljg%3D%3D'


class BrokerAPIView(APIView):
    def get(self, requset):
        queryset = Broker.objects.all()
        serializer = BrokerSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BrokerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ComplexViewSet(ModelViewSet):
    queryset = ComplexInformation.objects.all()
    serializer_class = ComplexInformationSerializer


class AddressViewSet(ModelViewSet):
    queryset = PostAddress.objects.all()
    serializer_class = AddressSerializer


class SalesFormViewSet(ModelViewSet):
    queryset = SalesForm.objects.all()
    serializer_class = SalesFormSerializer


class MaintenanceFeeViewSet(ModelViewSet):
    queryset = MaintenanceFee.objects.all()
    serializer_class = ManagementSerializer


class SecuritySafetyViewSet(ModelViewSet):
    queryset = SecuritySafetyFacilities.objects.all()
    serializer_class = SecuritySafetySerializer


class PostRoomViewSet(ModelViewSet):
    queryset = PostRoom.objects.all()

    def get_serializer_class(self):
        if self.action in "create":
            serializer_class = PostListSerializer
            return serializer_class

        else:
            serializer_class = PostListSerializer
            return serializer_class


class PostTestAPIVie(APIView):
    def post(self, request):
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            post_pk = serializer.data.get('pk')
            post = PostRoom.objects.get(pk=post_pk)

            # 이미지 relation  로직
            post_images = request.data.get('postimage')
            POSTS_IMAGE_DIR = os.path.join(MEDIA_ROOT, f'.posts/postroom{post_pk}/')
            if not os.path.exists(POSTS_IMAGE_DIR):
                os.makedirs(POSTS_IMAGE_DIR, exist_ok=True)
            for index, post_url in enumerate(post_images):
                #
                image_save_name = os.path.join(POSTS_IMAGE_DIR, f'{index}.jpg')
                urllib.request.urlretrieve(post_url, image_save_name)
                f = open(os.path.join(POSTS_IMAGE_DIR, f'{index}.jpg'), 'rb')
                PostImage.objects.create(
                    image=File(f),
                    post=post
                )
                f.close()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailTestAPIView(APIView):
    permission_classes = IsOwnerOrReadOnly

    def patch(self, request, pk):
        post = PostRoom.objects.get(pk=pk)
        serializer = PostCreateSerializer(post, data=request.data, partial=True, )
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = PostRoom.objects.get(pk=pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostTinytList(APIView):
    def get(self, request):
        queryset = PostRoom.objects.all()
        serializer = PostTinySerializer(queryset, many=True)
        return Response(serializer.data)


@api_view()
def getAptListService(request):
    secret_key = 'V8giduxGZ%2BU463maB552xw3jULhTVPrv%2B7m2qSqu4w8el9fk8bnMD9i6rjUQz7gcUcFnDKyOmcCBztcbVx3Ljg%3D%3D'
    url = "http://apis.data.go.kr/1611000/AptListService/getLegaldongAptList"
    bjd_code = request.data.get('bjdCode')
    if bjd_code == '성수동1가':
        bjd_code = '1120011400'
    elif bjd_code == '성수동2가':
        bjd_code = '1120011500'

    url_bjd = f'{url}?bjdCode={bjd_code}&ServiceKey={secret_key}'

    response = requests.get(url_bjd).content

    xmlObj = xmltodict.parse(response)
    json_data = json.dumps(xmlObj, ensure_ascii=False)
    dict_data = json.loads((json_data))
    data = dict_data['response']['body']['items']['item']
    return Response(data, status=status.HTTP_200_OK)


@api_view()
def getBorodCityList(request):
    url = f'http://openapi.epost.go.kr/postal/retrieveLotNumberAdressAreaCdService/' \
          f'retrieveLotNumberAdressAreaCdService/getBorodCityList?ServiceKey={secret}'
    response = requests.get(url).content
    xmlObj = xmltodict.parse(response)
    json_data = json.dumps(xmlObj, ensure_ascii=False)
    dict_data = json.loads((json_data))
    data = dict_data["BorodCityResponse"]["borodCity"]
    return Response(data, status=status.HTTP_200_OK)


@api_view()
def getSiGunGuList(request):
    brtcCd = request.data.get('brtcCd')
    url = f'http://openapi.epost.go.kr/postal/retrieveLotNumberAdressAreaCdService/' \
          f'retrieveLotNumberAdressAreaCdService/getSiGunGuList?ServiceKey={secret}&brtcCd={brtcCd}'
    response = requests.get(url).content
    xmlObj = xmltodict.parse(response)
    json_data = json.dumps(xmlObj, ensure_ascii=False)
    dict_data = json.loads((json_data))
    error = dict_data['SiGunGuListResponse']['cmmMsgHeader']['successYN']
    if error == 'N':
        data = {
            'message': '데이터가 올바르지 않습니다.'
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    data = dict_data['SiGunGuListResponse']['siGunGuList']
    return Response(data, status=status.HTTP_200_OK)


@api_view()
def getEupMyunDongList(request):
    brtcCd = request.data.get('brtcCd')
    signguCd = request.data.get('signguCd')
    url = f'http://openapi.epost.go.kr/postal/retrieveLotNumberAdressAreaCdService/' \
          f'retrieveLotNumberAdressAreaCdService/getEupMyunDongList?ServiceKey={secret}' \
          f'&brtcCd={brtcCd}&signguCd={signguCd}'
    response = requests.get(url).content
    xmlObj = xmltodict.parse(response)
    json_data = json.dumps(xmlObj, ensure_ascii=False)
    dict_data = json.loads((json_data))
    error = dict_data['EupMyunDongListResponse']['cmmMsgHeader']['successYN']
    if error == 'N':
        data = {
            'message': '데이터가 올바르지 않습니다.'
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    data = dict_data['EupMyunDongListResponse']['eupMyunDongList']
    return Response(data, status=status.HTTP_200_OK)


class PostLikeView(RetrieveAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def post(self, request):
        post_pk = request.query_params.get('post')
        post = get_object_or_404(PostRoom, pk=post_pk)
        serializer = PostLikeSerializer(
            data={'user': request.user.pk, 'post': post_pk}
        )
        if serializer.is_valid():
            if PostLike.objects.filter(
                    post=serializer.validated_data['post'],
                    user=request.user,
            ).exists():
                raise APIException('이미 좋아요 한 포스트 입니다.')
            serializer.save(user=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        post_pk = request.query_params.get('post')
        post = get_object_or_404(PostRoom, pk=post_pk)
        post_like = get_object_or_404(PostLike, post=post, user=request.user)
        post_like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
