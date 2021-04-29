from django.contrib import admin
from .models import Profile, Subject, Sub_Subject, Book, Question, Answer, Tag, Question_Tag


class BookAdmin(admin.ModelAdmin):
    model = Book
    list_display = ("book_name", "related_subject")


class SubSubjectAdmin(admin.ModelAdmin):
    model = Sub_Subject
    list_display = ("sub_subject_name", "related_subject")


class QuestionAdmin(admin.ModelAdmin):
    model = Question
    list_display = ("title", "subject", "profile", "publish_date")


class AnswerAdmin(admin.ModelAdmin):
    model = Answer
    list_display = ("profile", "question", "show_content")


admin.site.register(Profile)
admin.site.register(Subject)
admin.site.register(Sub_Subject, SubSubjectAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Tag)
admin.site.register(Question_Tag)
