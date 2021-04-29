from django.shortcuts import render
from .models import Question, Profile
from .forms import QuestionForm


def about(request):
    return render(request, 'home/about.html')


def landingpage(request):
    return render(request, 'home/landingpage.html')


def displayQuestion(request, **kwargs):
    question = Question.objects.all().get(id=kwargs['pk'])
    sortAnsBy = request.GET["sortanswersby"] if 'sortanswersby' in request.GET else ''
    context = {
        "question": question,
        "answers": question.get_answers_feed(sortAnsBy),
        "answersCount": question.answer_set.count(),
        "tags": question.tags.values(),
        "title": question.get_question_title()
    }
    return render(request, 'home/question_detail.html', context)


def new_question(request):
    form = QuestionForm
    if request.method == 'POST':
        questForm = QuestionForm(request.POST)
        if questForm.is_valid():
            questForm = questForm.save(commit=False)
            for currProfile in Profile.objects.all():
                if (currProfile.user == request.user):
                    questForm.profile = currProfile
                    break
            questForm.save()
    return render(request, 'home/questions/new_question.html', {'form': form, 'title': 'New Question'})
