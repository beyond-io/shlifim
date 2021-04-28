from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about, name='about'),
    path('', views.landingpage, name='landingpage'),
    path('explore/new_question', views.new_question, name='new_question')
]
