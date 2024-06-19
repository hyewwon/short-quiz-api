from rest_framework import serializers
from api.models import Quiz
from datetime import datetime

class QuizCreateSerializer(serializers.ModelSerializer):
    subjectId = serializers.IntegerField(required=True)
    class Meta:
        model = Quiz
        fields = ["title", "question", "options", "answer", "description"]