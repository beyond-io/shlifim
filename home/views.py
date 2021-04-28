from django.shortcuts import render
from .models import Question
from django_filters.views import FilterView
from django.db.models import Count


def about(request):
    return render(request, 'home/about.html')


def landingpage(request):
    return render(request, 'home/landingpage.html')


class QuestionsListView(FilterView):
    model = Question
    template_name = 'home/explore.html'
    context_object_name = 'questions'
    ordering = ['-publish_date']
    paginate_by = 10

    def get_paginate_by(self, queryset):
        return self.request.GET.get("paginate_by", self.paginate_by)

    def get_queryset(self):
        items_set = Question.objects.all()
        ordering = self.request.GET.get('order_by', '-publish_date')
        if ordering == "answersNum":
            items_set = items_set.annotate(answers_num=Count('answer')).order_by('-answers_num')
        else:
            items_set = items_set.order_by(ordering)

        return items_set
