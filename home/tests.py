from home.models import Profile, Subject, Question, Tag, Question_Tag
from django.contrib.auth.models import User
from django.utils import timezone
import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_add_tags_to_question(question_test_data):
    test_tags = ['test_tag_1', 'test_tag_2', 'test_tag_3']
    question_test_data.add_tags_to_question(test_tags)

    assert list(question_test_data.tags.values()) == [{'id': 5, 'tag_name': 'test_tag_1'},
                                                      {'id': 6, 'tag_name': 'test_tag_2'},
                                                      {'id': 7, 'tag_name': 'test_tag_3'}]


@pytest.mark.django_db
def test_field_questions_in_tag(question_tag_test_data):
    assert question_tag_test_data.questions.values().count() == 1


@pytest.mark.django_db
def test_question_tag_table(question_test_data, question_tag_test_data):
    assert Question_Tag.objects.filter(question=question_test_data, tag=question_tag_test_data).exists()


@pytest.mark.django_db
def test_add_tags_to_question_one_new_input(question_test_data, question_tag_test_data):
    question_test_data.add_tags_to_question(['test_tag_2', 'test_tag_3'])
    assert question_test_data.tags.values().count() == 2


@pytest.mark.django_db
def test_tags_feed_no_parameters():
    assert Tag.tags_feed().count() == 4


@pytest.mark.django_db
def test_tags_feed_with_test_tag(tag_test_data):
    assert tag_test_data.tags_feed().count() == 5


@pytest.mark.django_db
def test_tags_feed_with_filter(tag_test_data):
    assert Tag.tags_feed('_t').count() == 1


@pytest.mark.django_db
def test_tags_feed_after_delete(tag_test_data):
    Tag.objects.filter(tag_name='test_tag_1').delete()
    assert Tag.tags_feed().count() == 4


@pytest.mark.django_db
def test_tags_feed_no_result():
    assert Tag.tags_feed('testtesttesttest').count() == 0


@pytest.fixture
def question_test_data():
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
def tag_test_data():
    tag = Tag(tag_name='test_tag_1')
    tag.save()
    return tag


@pytest.fixture
def question_tag_test_data(question_test_data):
    test_tag = Tag()
    test_tag.tag_name = 'test_tag_2'
    test_tag.save()
    new_pair = Question_Tag()
    new_pair.question = question_test_data
    new_pair.tag = test_tag
    new_pair.save()
    return test_tag


@pytest.mark.django_db
@pytest.fixture
def explore_page_response(client):
    url = reverse('explore-page')
    response = client.get(url)
    return response


@pytest.mark.django_db
def test_explore_page_is_paginated(explore_page_response):
    assert (explore_page_response.context['is_paginated'] is True)
