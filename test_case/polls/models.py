from django.contrib.auth.models import User
from django.db import models
from rest_framework.exceptions import ValidationError


class Poll(models.Model):
    """
    Представление опроса
    """
    slug = models.SlugField(max_length=50, unique=True)
    title = models.CharField(max_length=100)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    """
    Представление вопросов в опросе
    """

    TEXT_INPUT = 'TXT'
    SINGLE_CHOICE = 'SCH'
    MULTIPLE_CHOICE = 'MCH'

    QUESTION_TYPE_CHOICES = [
        (TEXT_INPUT, 'Text input answer'),
        (SINGLE_CHOICE, 'Single choice'),
        (MULTIPLE_CHOICE, 'Multiple Choice'),
    ]

    number = models.PositiveSmallIntegerField()
    text = models.CharField(max_length=300)
    type = models.CharField(
        max_length=3,
        choices=QUESTION_TYPE_CHOICES,
        default=TEXT_INPUT,
    )
    poll = models.ForeignKey('Poll', on_delete=models.CASCADE, related_name='questions')

    class Meta:
        unique_together = ('poll', 'number')

    def __str__(self):
        return f'{self.number}. {self.text}'


class AnswerOption(models.Model):
    """
    Представление вариантов ответа для вопросов с выбором
    """
    text = models.CharField(max_length=300)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='options')

    class Meta:
        unique_together = ('text', 'question')

    def __str__(self):
        return f"{self.question.text}: * {self.text}"


class Answer(models.Model):
    """
    Представление ответов пользователей на вопросы
    """
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='answers')
    text = models.TextField(blank=True)
    chosen_answers = models.ManyToManyField('AnswerOption', blank=True)
    complete_time = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not (self.text or self.chosen_answers):
            raise ValidationError('Answer model must contain text or chosen answers')
