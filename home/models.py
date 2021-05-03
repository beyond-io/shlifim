from django.conf import settings
from django.db import models
from django.utils import timezone


class Gender(models.TextChoices):
    MALE = 'M', 'Male'
    FEMALE = 'F', 'Female'
    UNSPECIFIED = 'U', 'Unspecified'


class Profile(models.Model):
    '''
    Profile will be used as the base user in the Shlifim website.
    Profile is an extention to the imported 'User' from 'django.contrib.auth.models'.
    Imported Fields:
    username - Required. 150 characters or fewer. Usernames may contain alphanumeric, _, @, +, . and - characters.
    password - Required. A hash of, and metadata about, the password. (Django doesn’t store the raw password).
               Raw passwords can be arbitrarily long and can contain any character.
    date_joined - A datetime designating when the account was created. Is set to the current date/time by default
        when the account is created.
    email - Email address.
    is_superuser - Boolean. Designates that this user has all permissions without explicitly assigning them.
    Added Fields:
    gender - Default gender is set to 'Unspecified', A user can choose to specifie its gender to Male/Female.
    is blocked - Boolean. Designates that this user won't be able to login until an admin unblockes him.
    '''
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    gender = models.CharField(max_length=1, choices=Gender.choices, default=Gender.UNSPECIFIED)
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return '{self.user.username}'.format(self=self)


class Subject(models.Model):
    subject_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.subject_name


class Sub_Subject(models.Model):
    sub_subject_name = models.CharField(max_length=100)
    related_subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return self.sub_subject_name

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['sub_subject_name', 'related_subject'], name='unique_sub_subject')
        ]


class Book(models.Model):
    book_name = models.CharField(max_length=100, unique=True)
    related_subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return self.book_name


class Grade(models.TextChoices):
    GRADE7 = '7', 'Seventh Grade'
    GRADE8 = '8', 'Eighth grade'
    GRADE9 = '9', 'Ninth grade'
    GRADE10 = '10', 'Tenth grade'
    GRADE11 = '11', 'Eleventh grade'
    GRADE12 = '12', 'Twelfth grade'


class Question(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    publish_date = models.DateTimeField(default=timezone.now)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    sub_subject = models.ForeignKey(Sub_Subject, on_delete=models.CASCADE, blank=True, null=True)  # field not required
    grade = models.CharField(max_length=2, choices=Grade.choices)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)  # field not required
    book_page = models.IntegerField(null=True, blank=True)  # field not required
    is_edited = models.BooleanField(default=False)
    tags = models.ManyToManyField('Tag', through='Question_Tag')

    class Meta:
        ordering = ['-publish_date']  # default ordered by publish_date

    def __str__(self):
        return f"Question #{self.id} : {self.title} ( {self.publish_date.strftime('%d/%m/%Y %H:%M')} )"

    # Input: a set of strings represting tag names.
    def add_tags_to_question(self, tags):
        for tag_name in tags:
            # if tag exist in DB - fetch the tag. else, create a new tag.
            tag, created = Tag.objects.get_or_create(tag_name=tag_name)
            if created:
                tag.tag_name = tag_name
                tag.save()
            # add a new Question_Tag only if tag not in self.tags.
            if tag not in self.tags.all():
                new_pair = Question_Tag()
                new_pair.question = self
                new_pair.tag = tag
                new_pair.save()

    def get_answers_feed(self, filterType=''):
        '''
        Get all the answers in the DB for that question
        Also get filter type param for chosing between date / likes count filter
        '''
        answers = self.answer_set
        if filterType == 'date' or filterType == '':
            answers = answers.order_by('-publish_date')
        elif filterType == 'votes':
            answers = answers.order_by('-likes_count')
        return answers

    def get_question_title(self):
        return str(self.subject) + '-' + self.title

    def get_answers_num(self):
        return self.answer_set.count()


class Answer(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    publish_date = models.DateTimeField(default=timezone.now)
    likes_count = models.IntegerField(default=0)
    dislikes_count = models.IntegerField(default=0)
    is_edited = models.BooleanField(default=False)
    ordering = ['likes_count']

    def __str__(self):
        return self.content

    def thumb_up_answer(self):
        self.likes_count = self.likes_count + 1

    def thumb_down_answer(self):
        self.dislikes_count = self.dislikes_count + 1

    def set_is_edited(self, newVal):
        self.is_edited = newVal


class Tag(models.Model):
    tag_name = models.CharField(max_length=20)
    questions = models.ManyToManyField('Question', through='Question_Tag')

    def __str__(self):
        return self.tag_name

    # The function returnss all tags ordered by name tag.
    @classmethod
    def tags_feed(cls, search=''):
        return cls.objects.filter(tag_name__contains=search).order_by('tag_name')


class Question_Tag(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_ID')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='tag_ID')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['question', 'tag'], name='question_tag')
        ]

    def __str__(self):
        return f"{self.question}, Tag : {self.tag}"
