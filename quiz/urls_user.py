from django.contrib import admin
from django.urls import path, include
from .views_user import MyAPIView 

urlpatterns = [
    path('<int:exam_id>/', MyAPIView.as_view()),
    path('<int:exam_id>/ratings/', MyAPIView.as_view()),
    path('<int:exam_id>/standings/', MyAPIView.as_view()),
    path('<int:exam_id>/users/<int:userId>/answers/', MyAPIView.as_view()),    
    path('<int:exam_id>/users/<int:userId>/questions/next/', MyAPIView.as_view()),




    # path('api/', include('myapp.urls')),
]
