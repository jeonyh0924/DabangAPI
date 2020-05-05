import requests
from django.http import HttpResponse
from django.shortcuts import render

from config.settings.base import KAKAO_APP_ID


def login_page(request):
    context = {
        'user': request.user
    }
    return render(request, 'login.html', context)


def kakao_login(request):
    kakao_access_code = request.GET.get('code')
    url = 'https://kauth.kakao.com/oauth/token'
    headers = {
        'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
    }
    body = {
        'grant_type': 'authorization_code',
        'client_id': KAKAO_APP_ID,
        'redirect_url': 'https://moonpeter.com/members/kakao-login/',
        'code': kakao_access_code
    }
    kakao_reponse = requests.post(url, headers=headers, data=body)
    #  front 에서 받아야 할 역할 완료 /

    data = kakao_reponse.json()
    access_token = data['access_token']
    print('access token >>', access_token)
    url = 'https://kapi.kakao.com/v2/user/me'

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
    }
    kakao_response = requests.post(url, headers=headers)

    user_data = kakao_response.json()
    kakao_id = user_data['id']
    user_username = user_data['properties']['nickname']
    print(type(user_username))
    return HttpResponse(access_token)
