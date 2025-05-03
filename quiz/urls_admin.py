# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_admin import QuestionViewSet, QuestionSetViewSet, AnswerSetViewSet, QuestionSetViewSet2

router = DefaultRouter()
router.register(r'questions', QuestionViewSet, basename='question')
router.register(r'question-sets', QuestionSetViewSet, basename='question-set')
router.register(r'answer-sets', AnswerSetViewSet, basename='answer-set')
router.register(r'question-sets2', QuestionSetViewSet2, basename='question-set2')


urlpatterns = [
    path('', include(router.urls)),
]
