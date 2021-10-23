from rest_framework import serializers

from .models import Poll, Question, AnswerOption, Answer


class PollListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Poll
        fields = ('slug', 'title')


class AnswerOptionListSerializer(serializers.ListSerializer):
    """
    Сериализатор для множественного
    обновления вариантов ответа на вопрос.
    Если вложен вариант, который не
    связан с переданной сущностью, то
    метод создаст его
    """

    def update(self, instance, validated_data):
        opt_mapping = {option.text: option for option in instance.options.all()}
        sub_instances = []
        for opt_data in validated_data:
            if opt_data['text'] in opt_mapping:
                sub_instances.append(
                    self.child.update(opt_mapping[opt_data['text']], opt_data)
                )
            else:
                opt_data['question'] = instance
                sub_instances.append(self.child.create(opt_data))
        return sub_instances


class AnswerOptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnswerOption
        fields = ('text', )
        list_serializer_class = AnswerOptionListSerializer


class QuestionListSerializer(serializers.ListSerializer):
    """
    Сериализатор для множественного
    обновления вопросов в опросе.
    Если вложен вопрос, которого не
    связан с переданной сущностью,
    то метод создаст его
    """

    def update(self, instance, validated_data):
        q_mapping = {question.number: question for question in instance.questions.all()}
        sub_instances = []
        for q_data in validated_data:
            if q_data['number'] in q_mapping:
                sub_instances.append(self.child.update(q_mapping[q_data['number']], q_data))
            else:
                q_data['poll'] = instance
                sub_instances.append(self.child.create(q_data))
        return sub_instances


class QuestionSerializer(serializers.ModelSerializer):

    options = AnswerOptionSerializer(many=True)

    class Meta:
        model = Question
        fields = ('number', 'text', 'type', 'options')
        list_serializer_class = QuestionListSerializer

    def create(self, validated_data):
        """
        Переопределение создания сущности через сериализатор для
        создания вопроса с вложеннымми в него вариантами ответа
        """
        answer_options_validated_data = validated_data.pop('options')
        question = super().create(validated_data)
        options_serializer = self.fields['options']
        for each in answer_options_validated_data:
            each['question'] = question
        answer_options = options_serializer.create(answer_options_validated_data)
        return question

    def update(self, instance, validated_data):
        """
        Переопределение обновления сущности через сериализатор для
        создания вопроса с вложеннымми в него вариантами ответа
        """
        answer_options_validated_data = validated_data.pop('options')
        instance = super().update(instance, validated_data)
        options_serializer = self.fields['options']
        answer_options = options_serializer.update(instance, answer_options_validated_data)
        return instance


class PollDetailSerializer(serializers.ModelSerializer):

    questions = QuestionSerializer(many=True)

    class Meta:
        model = Poll
        fields = ('slug', 'title', 'start_date', 'end_date', 'questions')
        read_only_fields = ('start_date', )

    def create(self, validated_data):
        """
        Переопределение создания сущности через сериализатор для
        создания опроса с вложеннымми в него вопросами
        """
        questions_validated_data = validated_data.pop('questions')
        poll = super().create(validated_data)
        questions_serializer = self.fields['questions']
        for each in questions_validated_data:
            each['poll'] = poll
        questions = questions_serializer.create(questions_validated_data)
        return poll

    def update(self, instance, validated_data):
        """
        Переопределение обновления сущности через сериализатор для
        создания опроса с вложеннымми в него вопросами
        """
        questions_validated_data = validated_data.pop('questions')
        instance = super().update(instance, validated_data)
        questions_serializer = self.fields['questions']
        questions = questions_serializer.update(instance, questions_validated_data)
        return instance


class AnswerListSerializer(serializers.ModelSerializer):

    chosen_answers = AnswerOptionSerializer(many=True)
    question = serializers.StringRelatedField()

    class Meta:
        model = Answer
        fields = ('question', 'text', 'chosen_answers')


class PollResultSerializer(serializers.Serializer):
    """
    Сериализатор для обработки заполненной анкеты
    """
    poll = PollListSerializer()
    answers = AnswerListSerializer(many=True)
