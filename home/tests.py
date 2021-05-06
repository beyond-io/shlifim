from home.models import Profile, Subject, Question, Tag, Answer, Question_Tag
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from django.db.models.query import QuerySet
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed
import pytest
import pytz


class TestManyToManyFeature:
    @pytest.mark.django_db
    def test_add_tags_to_question(self, question_test_data):
        test_tags = ['test_tag_1', 'test_tag_2', 'test_tag_3']
        question_test_data.add_tags_to_question(test_tags)

        assert list(question_test_data.tags.values()) == [{'id': 5, 'tag_name': 'test_tag_1'},
                                                          {'id': 6, 'tag_name': 'test_tag_2'},
                                                          {'id': 7, 'tag_name': 'test_tag_3'}]

    @pytest.mark.django_db
    def test_field_questions_in_tag(self, question_tag_test_data):
        assert question_tag_test_data.questions.values().count() == 1

    @pytest.mark.django_db
    def test_question_tag_table(self, question_test_data, question_tag_test_data):
        assert Question_Tag.objects.filter(question=question_test_data, tag=question_tag_test_data).exists()

    @pytest.mark.django_db
    def test_add_tags_to_question_one_new_input(self, question_test_data, question_tag_test_data):
        question_test_data.add_tags_to_question(['test_tag_2', 'test_tag_3'])
        assert question_test_data.tags.values().count() == 2

    @pytest.mark.django_db
    def test_tags_feed_no_parameters(self):
        assert Tag.tags_feed().count() == 4

    @pytest.mark.django_db
    def test_tags_feed_with_test_tag(self, tag_test_data):
        assert tag_test_data.tags_feed().count() == 5

    @pytest.mark.django_db
    def test_tags_feed_with_filter(self, tag_test_data):
        assert Tag.tags_feed('_t').count() == 1

    @pytest.mark.django_db
    def test_tags_feed_after_delete(self, tag_test_data):
        Tag.objects.filter(tag_name='test_tag_1').delete()
        assert Tag.tags_feed().count() == 4

    @pytest.mark.django_db
    def test_tags_feed_no_result(self):
        assert Tag.tags_feed('testtesttesttest').count() == 0

    @pytest.fixture
    def question_test_data(self):
        user = User.objects.get(username='Rebecca')
        profile = Profile.objects.get(user=user)
        subject = Subject.objects.get(subject_name='Physics')
        question = Question(profile=profile,
                            title='Question test data',
                            content='Will this question test data pass?',
                            publish_date=timezone.now(),
                            subject=subject,
                            sub_subject=None,
                            grade='10',
                            book=None,
                            book_page=None,
                            is_edited=False)
        question.save()
        return question

    @pytest.fixture
    def tag_test_data(self):
        tag = Tag(tag_name='test_tag_1')
        tag.save()
        return tag

    @pytest.fixture
    def question_tag_test_data(self, question_test_data):
        test_tag = Tag()
        test_tag.tag_name = 'test_tag_2'
        test_tag.save()
        new_pair = Question_Tag()
        new_pair.question = question_test_data
        new_pair.tag = test_tag
        new_pair.save()
        return test_tag


class TestDisplayQuestionFeature:
    class TestAnswersManipulations:
        @pytest.fixture
        def answers(self):
            profile = Profile.objects.first()
            question = Question.objects.get(id=3)
            ans1 = Answer(profile=profile, question=question, content='Answer 1',
                          publish_date=datetime(2021, 4, 1, tzinfo=pytz.UTC),
                          likes_count=1, dislikes_count=0, is_edited=False)
            ans2 = Answer(profile=profile, question=question, content='Answer 2',
                          publish_date=datetime(2021, 4, 2, tzinfo=pytz.UTC),
                          likes_count=0, dislikes_count=0, is_edited=False)
            ans1.save()
            ans2.save()
            return [ans1, ans2]

        @pytest.mark.django_db
        def test_thumb_up_answer(self, answers):
            """
            thumb_up_answer(answer_id) increase the thumbs up field of an answer by one
            """
            prev_thumb_val = answers[0].likes_count
            answers[0].thumb_up_answer()
            assert(prev_thumb_val == answers[0].likes_count - 1)

        @pytest.mark.django_db
        def test_thumb_down_answer(self, answers):
            """
            thumb_down_answer(answer_id) increase the thumbs down field of an answer by one
            """
            prev_thumb_val = answers[0].dislikes_count
            answers[0].thumb_down_answer()
            assert(prev_thumb_val == answers[0].dislikes_count - 1)

        @pytest.mark.django_db
        def test_set_is_edited(self, answers):
            """
            Tests functionality of set_is_edited
            """
            prev_is_edited_val = answers[0].is_edited
            answers[0].set_is_edited(not prev_is_edited_val)
            assert(prev_is_edited_val != answers[0].is_edited)

        @pytest.mark.django_db
        @pytest.mark.parametrize(('filterType, expected'), [('date', 'Answer 2'), ('votes', 'Answer 1')])
        def test_answers_feed(self, filterType, expected, answers):
            """
            Tests if get_answers_feed returns queryset of all the answers of
            question number 3 sorted by votes or answers
            """
            question = Question.objects.get(id=3)
            answers_feed = question.get_answers_feed(filterType)
            assert isinstance(answers_feed, QuerySet)
            assert answers_feed[0].content == expected

    class TestQuestionRelatedMethods:
        @pytest.mark.django_db
        def test_get_question_title(self):
            """
            get_question_title(question_id) returns a string for question
            should return question subject and question title
            """
            question = Question.objects.get(id=1)
            assert(question.get_question_title() == "Math-question from math course")

    class TestHTMLRelated:
        @pytest.mark.django_db
        @pytest.fixture
        def response(self, client):
            url = reverse('question-detail', args=[14])
            response = client.get(url)
            return response

        @pytest.mark.django_db
        def test_display_question_page_url(self, response):
            """
            This test checks the returned status for routing to display-question feature
            """
            assert response.status_code == 200

        @pytest.mark.django_db
        def test_template_name(self, response):
            assert response.templates[0].name == "home/question_detail.html"

        @pytest.mark.django_db
        def test_response_context(self, response):
            '''
            Testing if the context passed to the view contains the right contents
            '''
            expectedPairs = [
                ('question', 'Question #14 : g forwards, it was even later than ( 28/04/2021 23:14 )'),
                ('answers', '<QuerySet [<Answer: Answer B>, <Answer: Answer A>,\
 <Answer: Popular Answer>, <Answer: Old Answer>]>'),
                ('answersCount', '4'),
                ('tags', '<QuerySet [{\'id\': 3, \'tag_name\': \'Bagrut_Exam\'},\
 {\'id\': 4, \'tag_name\': \'Hebrew\'}]>'),
                ('title', 'History-g forwards, it was even later than')
                ]
            for check, expected in expectedPairs:
                assert str(response.context[check]) == expected

        @pytest.mark.parametrize(('filterType, expected'), [('date', 'Answer B'), ('votes', 'Popular Answer')])
        @pytest.mark.django_db
        def test_sorting_answers(self, client, filterType, expected):
            url = f'/explore/question_14/?sortanswersby={filterType}'
            response = client.get(url)
            answer = response.context['answers'].first()
            assert str(answer.content) == expected


class TestTagsPage:
    @pytest.mark.django_db
    def test_tags_page_url(self, tags_response):
        assert tags_response.status_code == 200

    @pytest.mark.django_db
    def test_tags_page_context(self, tags_response):
        expected = '<QuerySet [<Tag: 5th_Grade>, <Tag: Bagrut_Exam>, <Tag: Hebrew>, <Tag: Pitagoras>]>'
        assert str(tags_response.context['tags']) == expected

    @pytest.mark.django_db
    def test_tags_page_template(self, tags_response):
        assertTemplateUsed(tags_response, 'home/tags.html')

    @pytest.fixture
    def tags_response(self, client):
        url = reverse('tags')
        response = client.get(url)
        return response
