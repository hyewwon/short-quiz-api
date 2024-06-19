from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

from django.db.models import F
from django.db import transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from django.contrib.auth.models import User

from api.serializers.auth_serializers import MyTokenObtainPairSerializer, MyTokenRefreshSerializer, RefreshTokenIDSerializer, RefreshTokenSerializer, OAuthLoginSerializer, UserSerializer
import requests


class LoginView(GenericAPIView):
    '''
        로그인 API
    '''
    permission_classes = [AllowAny]
    serializer_class = OAuthLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            access_token = serializer.validated_data["access_token"]

            user_info_req = requests.get(f"https://www.googleapis.com/oauth2/v3/userinfo?access_token={access_token}")

            if not user_info_req.ok:
                    return Response({"message" : "잘못된 토큰 정보입니다."}, status=status.HTTP_400_BAD_REQUEST)

            user_info = user_info_req.json()
            email = user_info.get("email")
            profile_image = user_info.get("picture", "")

            try:
                user = User.objects.get(username=email, email=email)
            except:
                user = User.objects.create(
                    username = email,
                    email = email
                )
                user.profile.profile_image = profile_image
                user.save()
            
            token = MyTokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            outstandingToken = OutstandingToken.objects.get(token = refresh_token)
            response = Response(
                {   
                    "user" : UserSerializer(user).data,
                    "message":"로그인 되었습니다.",
                    "jwt_token" :{
                        "access_token" : access_token,
                        "refresh_token_index_id": outstandingToken.id,
                        "refresh_token_exp" : outstandingToken.expires_at.timestamp()
                    }
                },
                status=status.HTTP_200_OK                
            )
            return response
        


class ReissueTokenView(GenericAPIView):
    '''
        refresh 토큰 재발급 api
    '''
    permission_classes = [AllowAny]
    serializer_class = RefreshTokenIDSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception = True):
            refresh_token_index_id = serializer.validated_data["refresh_token_index_id"]
            try:
                refresh = OutstandingToken.objects.get(pk = refresh_token_index_id)
            except:
                return Response(
                    {"message": "refresh token 정보 오류"}, status=status.HTTP_400_BAD_REQUEST
                )

            serializer = MyTokenRefreshSerializer(data={"refresh": refresh.token})
            serializer.is_valid(raise_exception=True)
            refresh_token = serializer.validated_data["refresh"]
            access_token = serializer.validated_data["access"]
            outstandingToken = OutstandingToken.objects.get(token=refresh_token)
            response = Response(
                {
                    "user" : UserSerializer(refresh.user).data,
                    "message": "refresh token reissue",
                    "jwt token" : {
                        "access_token" : access_token,
                        "refresh_token_index_id" : outstandingToken.id,
                        "refresh_token_exp" : outstandingToken.expires_at.timestamp()
                    }
                },
                status=status.HTTP_200_OK
            )

            return response


class LogoutView(GenericAPIView):
    '''
        로그아웃 API
    '''
    permission_classes = [IsAuthenticated]
    serializer_class = RefreshTokenIDSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception = True):
            refresh_token_index_id = serializer.validated_data["refresh_token_index_id"]
            try:
                refresh = OutstandingToken.objects.get(pk = refresh_token_index_id)
            except:
                return Response({"message":"refresh token does not exist"}, status=status.HTTP_400_BAD_REQUEST)

            serializer = RefreshTokenSerializer(data={'refresh':refresh.token})
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(status=status.HTTP_204_NO_CONTENT)

    
