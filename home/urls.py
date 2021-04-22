from django.urls import path
from . import views
from .views import QuestionsListView

urlpatterns = [
    path('about/', views.about, name='about'),
    path('', views.landingpage, name='landingpage'),
    path('explore/', QuestionsListView.as_view(), name='explore-page')
]
