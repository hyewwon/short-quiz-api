from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from django.views.generic import View
from django.http import HttpRequest, JsonResponse
from django.conf import settings
import requests


class GoogleLoginView(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        client_id = settings.GOOGLE_OAUTH2_CLIENT_ID
        scope = "https://www.googleapis.com/auth/userinfo.email " + \
                "https://www.googleapis.com/auth/userinfo.profile"
        
        redirect_uri = f"http://127.0.0.1:8000/api/google/login/callback/"
        google_auth_api = "https://accounts.google.com/o/oauth2/v2/auth"
        
        response = redirect(
            f"{google_auth_api}?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scope}"
        )
        
        return response


class GoogleLoginCallbackView(View):

    def get(self, request: HttpRequest, *args, **kwargs):
        client_id = settings.GOOGLE_OAUTH2_CLIENT_ID
        client_secret = settings.GOOGLE_OAUTH2_CLIENT_SECRET_KEY

        code = request.GET.get('code')
        grant_type = 'authorization_code'
        redirect_uri = f"http://127.0.0.1:8000/api/google/login/callback/"
        state = "state"

        google_token_api = f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type={grant_type}&redirect_uri={redirect_uri}&state={state}"
        token_response = requests.post(google_token_api)
        if not token_response.ok:
            return JsonResponse({"message" : "유효하지 않은 토큰"}, status=400)
        
        access_token = token_response.json().get('access_token')
        print("access_token : ", access_token)

        user_info_url = f"https://www.googleapis.com/oauth2/v3/userinfo?access_token={access_token}"
        user_info_response = requests.get(url=user_info_url)
        if not user_info_response.ok:
            return JsonResponse({"message" : "유저 정보 조회 실패"}, status=400)
        

        return JsonResponse(user_info_response.json(), status=200)

 
