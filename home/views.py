from django.shortcuts import render
from .forms import QuestionForm
from .models import Profile


def about(request):
    return render(request, 'home/about.html')


def landingpage(request):
    return render(request, 'home/landingpage.html')


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
