from django.urls import path, include
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', include('quiz.urls_admin')),
    path('exams/', include('quiz.urls_user')),
    path('rank/<int:exam_id>/', views.get_rank, name='get_rank'),
    path('start/<int:user_id>/<int:exam_id>/', views.start_exam, name='start_exam'),
    path('get_question/<int:user_id>/<int:exam_id>/', views.get_question, name='get_question'),
    path('submit_question/<int:user_id>/<int:exam_id>/<str:selected_answer>/', views.submit_question, name='submit_question'),
    path('get_short_rank/<int:user_id>/<int:exam_id>/', views.get_short_rank, name='get_short_rank'),
    path('set_user/', views.get_or_create_user_with_incremented_id ),
    
]
# submit_question