from django.shortcuts import render
from .models import Question
from django_filters.views import FilterView


def about(request):
    return render(request, 'home/about.html')


def landingpage(request):
    return render(request, 'home/landingpage.html')


class QuestionsListView(FilterView):
    model = Question
    template_name = 'home/explore.html'
    context_object_name = 'questions'
    ordering = ['-publish_date']
