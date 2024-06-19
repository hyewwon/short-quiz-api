from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.state import token_backend
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from django.contrib.auth.models import User
from api.models import Profile
from datetime import datetime

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["profile_image"]


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    class Meta:
        model = User
        fields = ("id", "username", "profile")
    

class OAuthLoginSerializer(serializers.Serializer):
    access_token = serializers.CharField(required=True)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token =  super().get_token(user)

        return token


class MyTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = serializers.CharField()
    access = serializers.CharField(read_only=True)
    token_class = RefreshToken

    def validate(self, attrs):
        verify_refresh(self.token_class(attrs["refresh"]))
        data = super(MyTokenRefreshSerializer, self).validate(attrs) # return payload 정보, refresh, access 정보?
        decoded_payload = token_backend.decode(data['refresh'], verify=True)
        user_uid=decoded_payload['user_id']
        jti=decoded_payload['jti']
        exp=decoded_payload['exp']
        OutstandingToken.objects.create(
            user=User.objects.get(pk=user_uid),
            jti=jti,
            expires_at = datetime.fromtimestamp(exp),
            token = str(data['refresh']),
            created_at=datetime.utcnow(),
        )

        return data


class RefreshTokenIDSerializer(serializers.Serializer):
    refresh_token_index_id = serializers.IntegerField(required=True)


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        "bad_token" : ("Token is invalid or expired")
        }

    def validate(self, attrs):
        self.token = attrs["refresh"]
        return attrs
    
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError: 
            self.fail("bad token")


def verify_refresh(refresh_token):
    try:
        token = OutstandingToken.objects.get(token=str(refresh_token))
    except OutstandingToken.DoesNotExist:
        raise serializers.ValidationError("Invalid Token")

    return token
        