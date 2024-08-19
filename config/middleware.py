
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.state import token_backend

class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_auth = str(request.headers.get('Authorization'))
        if request_auth and request_auth.startswith('Bearer '):
            access_token = request_auth.split(' ')[1]
        else:
            return Response({"message" : "사용자 토큰 정보 오류"}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            decoded_payload = token_backend.decode(access_token, verify=True)
            user_id = decoded_payload['user_id']
            user = User.objects.get(pk= user_id)
        except User.DoesNotExist:
            return Response({"message" : "사용자 정보가 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)

        request.user = user     
        response = self.get_response(request)

        return response