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
from api.utils import getUser
from api.models import SolvedQuiz, QuizLike, Quiz, QuizSubject
import requests


class SolvedQuizListView(APIView):
    '''
        내가 푼 퀴즈 리스트
    '''
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user = getUser(token = str(request.auth))
        if not user:
            return Response({"message" : "사용자 정보 오류"}, status=status.HTTP_401_UNAUTHORIZED)
        
        solved_quiz = SolvedQuiz.objects.filter(user=user).values(
            "quiz__subject", 
            "quiz__title", 
            "quiz__question", 
            "quiz__question_image"
        ).order_by("-solved_at")
        
        return Response({"message": "내가 푼 퀴즈 리스트", "solvedQuizList" : solved_quiz}, status=status.HTTP_200_OK) 
    

class LikeQuizListView(APIView):
    '''
        내가 좋아요한 퀴즈 리스트
    '''
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user = getUser(token=str(request.auth))
        if not user:
            return Response({"message" : "사용자 정보 오류"}, status=status.HTTP_401_UNAUTHORIZED)
        
        like_quiz = QuizLike.objects.filter(user = user)

        return Response({"message": "내가 좋아요한 퀴즈 리스트", "likeQuizList" : like_quiz}, status=status.HTTP_200_OK)
    

class MyQuizListView(APIView):
    '''
        내가 만든 퀴즈 리스트
    '''
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user = getUser(token=str(request.auth))
        if not user:
            return Response({"message" : "사용자 정보 오루"}, status=status.HTTP_401_UNAUTHORIZED)
        
        quiz = Quiz.objects.filter(user=user)

        return Response({"message" : "내가 만든 퀴즈 리스트", "myQuizList" : quiz}, status=status.HTTP_200_OK)
    

class QuizSubjectListView(APIView):
    '''
        퀴즈 주제 리스트
    '''
    def get(self, request, *args, **kwargs):
        user = getUser(token=str(request.auth))
        if not user:
            return Response({"message" : "사용자 정보 오루"}, status=status.HTTP_401_UNAUTHORIZED)

        subject = QuizSubject.objects.all().values("id", "subject")

        return Response({"message" : "퀴즈 주제 리스트", "quizSubjectList": subject}, status=status.HTTP_200_OK)



class QuizDeleteView(APIView):
    '''
        퀴즈 삭제
    '''
    permission_classes = [IsAuthenticated]
    def delete(self, request, *args, **kwargs):
        user = getUser(token=str(request.auth))
        if not user:
            return Response({"message" : "사용자 정보 오루"}, status=status.HTTP_401_UNAUTHORIZED)
        
        quiz_id = request.POST.get("pk")
        try:
            quiz = Quiz.objects.get(user=user, pk=quiz_id)
        except:
            return Response({"message" : "잘못된 퀴즈 정보입니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            quiz.delete()
        except:
            return Response({"message" : "퀴즈 삭제 실패. 관리자에게 문의해주세요!"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message" : "삭제 되었습니다."}, status=status.HTTP_202_ACCEPTED)
    

class QuizCreateView(APIView):
    '''
        퀴즈 생성
    '''
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        user = getUser(token=str(request.auth))
        if not user:
            return Response({"message" : "사용자 정보 오루"}, status=status.HTTP_401_UNAUTHORIZED)



