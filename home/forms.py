from django import forms
from .models import Question


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('title', 'subject', 'sub_subject', 'grade', 'book', 'book_page', 'content')
