from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('about/', views.about, name='about'),
    path('', views.landingpage, name='landingpage'),
    path('explore/question_<int:pk>/', views.displayQuestion, name='question-detail'),
    path('tags/', views.tags, name='tags'),
    path('logout/', auth_views.LogoutView.as_view(template_name='home/logout.html'), name='logout'),
]
