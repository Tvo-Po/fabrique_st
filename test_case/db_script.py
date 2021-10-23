import os, django
from random import randint, choice, sample

from django.db import IntegrityError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_case.settings')
django.setup()

import asyncio

from polls.models import Poll, Question, AnswerOption, Answer
from script_utils import generate_words, generate_poll_period


def generate_choices(question, question_type):
    choices = []
    for i in range(randint(3, 7)):
        choice_text = generate_words(2, 7)
        choice_text += '.'
        aw_choice = AnswerOption.objects.get_or_create(
            text=choice_text, question=question
        )
        if aw_choice[1]:
            aw_choice = aw_choice[0]
            choices.append(aw_choice)
    return choices


def generate_questions(poll, users):
    for i in range(randint(7, 14)):
        types = ("TXT", "SCH", "MCH")
        question_text = generate_words(5, 15)
        question_text += '?'
        question_type = types[randint(0, 2)]
        number = i + 1
        question = Question.objects.get_or_create(
            number=number, type=question_type,
            text=question_text, poll=poll
        )
        if question[1]:
            question = question[0]
        else:
            continue
        if question_type != "TXT":
            choices = generate_choices(question, question_type)
            for _ in range(randint(1, 7)):
                if question_type == "SCH":
                    user_choice = [choice(choices)]
                else:
                    user_choice = sample(choices, randint(1, len(choices)))
                answer_option = Answer.objects.get_or_create(
                    user=users[randint(0, 3)], question=question
                )
                if answer_option[1]:
                    answer_option = answer_option[0]
                else:
                    continue
                answer_option.chosen_answers.set(user_choice)
                answer_option.save()
        else:
            for _ in range(randint(1, 7)):
                user_text = generate_words(5, 45)
                user_text += '.'
                answer_option = Answer.objects.get_or_create(
                    user=users[randint(0, 3)], question=question, text= user_text
                )


async def populate():
    print('DB population begins...')
    printed_waiting = 0
    tries_amount = 60
    users = None
    try:
        admin = django.contrib.auth.models.User.objects.create_user(username='admin', password='admin', is_staff=True)
    except IntegrityError:
        admin = django.contrib.auth.models.User.objects.get(username='admin')
    try:
        user1 = django.contrib.auth.models.User.objects.create_user(username='riddler', password='riddler', is_active=True)
    except IntegrityError:
        user1 = django.contrib.auth.models.User.objects.get(username='riddler')
    try:
        user2 = django.contrib.auth.models.User.objects.create_user(username='advisor', password='advisor', is_active=True)
    except IntegrityError:
        user2 = django.contrib.auth.models.User.objects.get(username='advisor')
    try:
        user3 = django.contrib.auth.models.User.objects.create_user(username='bear', password='bear', is_active=True)
    except IntegrityError:
        user3 = django.contrib.auth.models.User.objects.get(username='bear')
    finally:
        users = (admin, user1, user2, user3)

    for i in range(tries_amount):
        poll_title = generate_words(2, 4)
        poll_slug = poll_title.lower().replace(" ", "_")
        poll_start_date, poll_end_date = generate_poll_period()
        if poll_slug == 'Dump mock':
            continue
        poll = Poll.objects.get_or_create(
            slug=poll_slug, title=poll_title,
            start_date=poll_start_date,
            end_date=poll_end_date
        )
        if poll[1]:
            poll = poll[0]
        else:
            continue
        generate_questions(poll, users)
        if i / tries_amount >= 0.25 and printed_waiting == 0:
            print('.....25%')
            printed_waiting = 1
        if i / tries_amount >= 0.50 and printed_waiting == 1:
            print('............50%')
            printed_waiting = 2
        if i / tries_amount >= 0.75 and printed_waiting == 1:
            print('....................75%')
            printed_waiting = 3
    print('DB population ends...')

asyncio.run(populate())