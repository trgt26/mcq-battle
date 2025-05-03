# views.py
from rest_framework import viewsets
from .models import Question, QuestionSet, AnswerSet
from .serializers_admin import QuestionSerializer, QuestionSetSerializer, AnswerSetSerializer, QuestionSetListSerializer, QuestionSetUpdateSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class QuestionSetViewSet(viewsets.ModelViewSet):
    queryset = QuestionSet.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'create':
            return QuestionSetListSerializer
        elif self.action == 'update':
            return QuestionSetUpdateSerializer
        
        return QuestionSetSerializer

class QuestionSetViewSet2(viewsets.ModelViewSet):
    queryset = QuestionSet.objects.all()
    serializer_class = QuestionSetSerializer

class AnswerSetViewSet(viewsets.ModelViewSet):
    queryset = AnswerSet.objects.all()
    serializer_class = AnswerSetSerializer

