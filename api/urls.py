from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenVerifyView
from api.views.auth.auth_views import LoginView, ReissueTokenView, LogoutView
from api.views.auth.test_oauth import GoogleLoginView, GoogleLoginCallbackView
app_name = "api"

urlpatterns = [
    path('auth/login/', LoginView.as_view()),
    path('token/verify/', TokenVerifyView.as_view()), #토큰 검증 
    path('token/refresh/', ReissueTokenView.as_view()),
    path('logout/', LogoutView.as_view()),

    path('google/login/', GoogleLoginView.as_view(), name='google_login'),
    path('google/login/callback/', GoogleLoginCallbackView.as_view(), name='google_login_callback'),

]
