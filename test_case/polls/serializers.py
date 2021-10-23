from rest_framework import serializers

from test_case.polls.models import Poll, Question, AnswerOption


class PollListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Poll
        fields = ('slug', 'title')


class AnswerOptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnswerOption
        fields = ('text', )


class QuestionSerializer(serializers.ModelSerializer):

    options = AnswerOptionSerializer(many=True)

    class Meta:
        model = Question
        fields = ('number', 'text', 'type', 'options')


class PollDetailSerializer(serializers.ModelSerializer):

    questions = QuestionSerializer(many=True)

    class Meta:
        model = Poll
        fields = ('slug', 'title', 'start_date', 'end_date', 'questions')
        read_only_fields = ('start_date', )
