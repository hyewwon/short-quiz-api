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

from api.serializers.auth_serializers import MyTokenRefreshSerializer, RefreshTokenIDSerializer, LogoutSerializer, OAuthLoginSerializer, UserSerializer


class LoginView(GenericAPIView):
    '''
        로그인 API
    '''
    permission_classes = [AllowAny]
    serializer_class = OAuthLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.save()
            data['message'] = '로그인 되었습니다.'
            return Response(data, status=status.HTTP_200_OK)
        
        return Response({'message' : serializer.error}, status=status.HTTP_400_BAD_REQUEST)


class ReissueTokenView(GenericAPIView):
    '''
        refresh 토큰 재발급 api
    '''
    permission_classes = [AllowAny]
    serializer_class = RefreshTokenIDSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        refresh = serializer.validated_data['refresh']

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
            refresh = serializer.validated_data['refresh']
            logout_serializer = LogoutSerializer(data={'refresh' : refresh.token})
            logout_serializer.is_valid(raise_exception=True)
            logout_serializer.save()
            return Response({'message' : '로그아웃 되었습니다.'}, status=status.HTTP_200_OK)
        
        return Response({'message' : '로그아웃 실패. 관리자에게 문의해주세요.'}, status=status.HTTP_400_BAD_REQUEST)

    
