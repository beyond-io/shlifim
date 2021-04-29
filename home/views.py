from django.shortcuts import render, redirect, reverse
from .models import Profile, Question, Tag
from .forms import CommentForm


def about(request):
    return render(request, 'home/about.html')


def landingpage(request):
    return render(request, 'home/landingpage.html')


def displayQuestionPage(request, **kwargs):
    form = CommentForm(request.POST)
    question = Question.objects.all().get(id=kwargs['pk'])
    sortAnsBy = request.GET["sortanswersby"] if 'sortanswersby' in request.GET else ''
    context = {
        "question": question,
        "answers": question.get_answers_feed(sortAnsBy),
        "answersCount": question.answer_set.count(),
        "tags": question.tags.values(),
        "title": question.get_question_title(),
        "form": form
    }
    if request.method == 'POST':
        profile = Profile.objects.filter(user=request.user).first()
        return addAnswer(form, profile, question)
    return render(request, 'home/question_detail.html', context)


def tags(request):
    if 'q' in request.GET:
        search = request.GET['q']
        tags = Tag.tags_feed(search)
    else:
        tags = Tag.tags_feed()
    return render(request, 'home/tags.html', {'tags': tags})

def addAnswer(form, profile, question):
    if form.is_valid():
        form.instance.profile = profile
        form.instance.question = question
        form.save()
        return redirect(reverse("question-detail", kwargs={
            'pk': question.pk
        }))
