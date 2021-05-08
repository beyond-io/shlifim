from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about, name='about'),
    path('', views.landingpage, name='landingpage'),
    path('explore/question_<int:pk>/', views.displayQuestion, name='question-detail'),
    path('tags/', views.tags, name='tags'),
    path('explore/new_question', views.new_question, name='new_question')
]
