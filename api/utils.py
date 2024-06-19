from django.contrib.auth.models import User
from rest_framework_simplejwt.state import token_backend

def getUser(token:str):
    try:
        decoded_payload = token_backend.decode(token, verify=True)
        user_udi = decoded_payload["user_id"]
        user = User.objects.get(pk = user_udi)
    except:
        user = None

    return user
