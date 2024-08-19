from django.contrib.auth.models import User
from rest_framework_simplejwt.state import token_backend
import requests

def getUser(token:str):
    try:
        decoded_payload = token_backend.decode(token, verify=True)
        user_udi = decoded_payload["user_id"]
        user = User.objects.get(pk = user_udi)
    except:
        user = None

    return user


def getGoogleUserInfo(token):
    '''
        구글 토큰으로 유저 정보 조회
    '''
    user_data = {}
    user_info_req = requests.get(f"https://www.googleapis.com/oauth2/v3/userinfo?access_token={token}")

    if not user_info_req.ok:
        return user_data

    else:
        user_info = user_info_req.json()
        user_data['email'] = user_info.get('email')
        user_data['profile_image'] = user_info.get('picture')
        return user_data
    

