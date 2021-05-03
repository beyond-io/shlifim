import django_filters
from .models import Question


class QuestionFilter(django_filters.FilterSet):
    book_page_filter = django_filters.NumberFilter(field_name='book_page', max_value=9999, min_value=1)

    class Meta:
        model = Question
        fields = ['subject', 'sub_subject', 'grade', 'book', 'book_page_filter']
