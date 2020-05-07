from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from posts.serializers import PostListSerializer, BrokerSerializer, PostLikeUserSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'pk',
            'username',
            'password',
            'email',
            'profileImage'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value: str):
        return make_password(value)


class UserProfileSerializer(serializers.ModelSerializer):
    posts = PostListSerializer(many=True, read_only=True)
    brokers = BrokerSerializer(many=True, read_only=True, )
    postLike = PostLikeUserSerializer(source='postlike_set', many=True, read_only=True, )

    class Meta:
        model = User
        fields = [
            'pk',
            'phone',
            'email',
            'profileImage',
            'posts',
            'brokers',
            'postLike',
        ]
