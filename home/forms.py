from django import forms
from .models import Answer
from ckeditor.fields import RichTextField


class CommentForm(forms.ModelForm):

    content = RichTextField(blank=True, null=True)

    class Meta:
        model = Answer
        fields = ('content',)
