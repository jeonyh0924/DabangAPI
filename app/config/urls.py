"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token

from config import settings
from members import views
from members.urls import urlpatterns_members
from posts.urls import urlpatterns_posts
from presales.urls import urlpatterns_presales

urlpatterns = [
    # path('auth/', include('rest_framework_social_oauth2.urls')), # rest_framework_social_oauth2

    path('api/token/', obtain_jwt_token),  # djangorestframework-jwt
    path('api/token/verify/', verify_jwt_token),  # djangorestframework-jwt
    path('api/token/refresh/', refresh_jwt_token),  # djangorestframework-jwt

    path('admin/', admin.site.urls),
    path('members/', include(urlpatterns_members)),
    path('posts/', include(urlpatterns_posts)),
    path('presales/', include(urlpatterns_presales)),
    path('login/', views.login_page, name='login-page'),  # kakao access token 받기 위한 template
]

urlpatterns += static(settings.base.MEDIA_URL, document_root=settings.base.MEDIA_ROOT)

if settings.dev.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
