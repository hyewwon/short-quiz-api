from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.state import token_backend
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.utils import datetime_from_epoch
from django.contrib.auth.models import User
from api.models import Profile
from datetime import datetime
from api.utils import getGoogleUserInfo
import requests

# 토큰 생성
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token =  super().get_token(user)

        return token

# 로그인
class OAuthLoginSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)

    def validate(self, attrs):
        token = attrs.get("token")
        
        user_data = getGoogleUserInfo(token)
        if not user_data:
            raise serializers.ValidationError('구글 토큰이 유효하지 않습니다.')
        try:
            user = User.objects.get(username=user_data['email'], email=user_data['email'])
        except:
            user = User.objects.create(
                username = user_data['email'],
                email = user_data['email']
            )
            user.profile.profile_image = user_data['profile_image']
            user.save()

        attrs['user'] = user
        return attrs
    
    def create(self, validated_data):
        user = validated_data.get('user', '')
        token = MyTokenObtainPairSerializer.get_token(user)
        verify_refresh_by_token(str(token))
        return {
            "user" : UserSerializer(user).data,
            "jwt_token" : {
                "access_token" : str(token.access_token),
                "refresh_token": str(token),
                "refresh_token_exp" : token["exp"]
            }
        }


# 토큰 재발행
class MyTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = serializers.CharField()
    access = serializers.CharField(read_only=True)
    token_class = RefreshToken # 발급된 refresh token 확인

    def validate(self, attrs):
        data = super(MyTokenRefreshSerializer, self).validate(attrs)
        decoded_payload = token_backend.decode(data['refresh'], verify=True)
        user_uid=decoded_payload['user_id']
        jti=decoded_payload['jti']
        exp=decoded_payload['exp']
        OutstandingToken.objects.create(
            user=User.objects.get(pk=user_uid),
            jti=jti,
            expires_at = datetime_from_epoch(exp),
            token = str(data['refresh']),
            created_at=data['refresh'].current_time,
        )
        
        return data

# refresh 조회
class RefreshTokenIDSerializer(serializers.Serializer):
    refresh_token_index_id = serializers.IntegerField(required=True)

    def validate(self, attrs):
        refresh_token_index_id = attrs.get('refresh_token_index_id')
        refresh = verify_refresh_by_id(refresh_token_index_id)
        attrs['refresh'] = refresh
        return attrs


# 로그아웃
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        "bad_token" : ("토큰이 유효하지 않습니다.")
        }

    def validate(self, attrs):
        self.token = attrs["refresh"]
        return attrs
    
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError: 
            self.fail("유효하지 않은 토큰")


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["profile_image"]


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    class Meta:
        model = User
        fields = ("id", "username", "profile")


def verify_refresh_by_token(refresh_token):
    try:
        OutstandingToken.objects.get(token=str(refresh_token))
    except OutstandingToken.DoesNotExist:
        raise serializers.ValidationError("Invalid Token")


def verify_refresh_by_id(id):
    try:
        token = OutstandingToken.objects.get(pk = id)
    except OutstandingToken.DoesNotExist:
        raise serializers.ValidationError("Invalid Token")
    
    return token
        
