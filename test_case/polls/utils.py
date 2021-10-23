from django.db.models import Q
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import Answer, AnswerOption


def validate_and_create_answer_form(answer_data, question):
    answer, chosen_answers = None, None
    if question.type == 'TXT':
        answer, chosen_answers = validate_and_create_text_answer(answer_data, question)
    elif question.type == 'SCH':
        answer, chosen_answers = validate_and_create_single_choice_answer(answer_data, question)
    elif question.type == 'MCH':
        answer, chosen_answers = validate_and_create_multiple_choice_answer(answer_data, question)
    else:
        ValidationError('Invalid question type')
    return answer, chosen_answers


def validate_and_create_text_answer(answer_data, question):
    answer, chosen_answers = None, None
    answer_text = answer_data.get('text')
    if answer_text is None:
        raise ValidationError('You must write something in text answer')
    answer = Answer(text=answer_text, question=question)
    return answer, chosen_answers


def validate_and_create_single_choice_answer(answer_data, question):
    answer, chosen_answers = None, None
    chosen_option = answer_data.get('chosen_answers')[0]
    if chosen_option is None:
        ValidationError('You must enter chosen_option in single choice question')
    option_text = chosen_option.get('text')
    if option_text is None:
        ValidationError('You must enter text for chosen option')
    try:
        chosen_answers = [AnswerOption.objects.get(question=question, text=option_text)]
    except AnswerOption.DoesNotExist:
        Response(status=400)
    else:
        answer = Answer(question=question)
    return answer, chosen_answers


def validate_and_create_multiple_choice_answer(answer_data, question):
    answer, chosen_answers = None, None
    chosen_options = answer_data.get('chosen_answers', [])
    if not chosen_options:
        ValidationError('You must enter chosen_options in multiple choice question')
    try:
        options = [option['text'] for option in chosen_options]
    except KeyError:
        raise ValidationError('You must enter text for chosen options')
    else:
        chosen_answers = AnswerOption.objects.filter(
            Q(question=question) & Q(text__in=options)
        )
        if len(chosen_answers) < len(options):
            raise ValidationError('You enter uncorrected text for chosen answers')
        answer = Answer(question=question)
    return answer, chosen_answers