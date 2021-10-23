import datetime

from django.db.models import Q, QuerySet
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (ListAPIView, GenericAPIView,
                                     get_object_or_404,
                                     RetrieveAPIView, CreateAPIView)
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Poll, Answer, Question
from .pagination import StandardResultsSetPagination
from .serializers import (PollListSerializer,
                          PollDetailSerializer,
                          PollResultSerializer)
from .utils import validate_and_create_answer_form


class PollsCurrentListView(ListAPIView):
    """
    Выводит список опросов,
    которые еще не закончились
    """
    serializer_class = PollListSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        self.queryset = Poll.objects.filter(
            Q(end_date__gte=datetime.datetime.today()) | Q(end_date=None)
        )
        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            queryset = queryset.all()
        return queryset


class PollRetrieveView(RetrieveAPIView):
    """
    Выводит подробную информацию об опросе
    """
    queryset = Poll.objects.all()
    serializer_class = PollDetailSerializer
    lookup_field = 'slug'


class PollAdminCreateView(CreateAPIView):
    """
    Функционал создания опроса для администратора
    """
    permission_classes = [IsAdminUser]
    queryset = Poll.objects.all()
    serializer_class = PollDetailSerializer


class PollAdminEditView(UpdateModelMixin,
                        DestroyModelMixin,
                        GenericAPIView):
    """
    Функционал редактирования (обновление,
    удаление) опроса для администратора
    """
    permission_classes = [IsAdminUser]
    queryset = Poll.objects.all()
    serializer_class = PollDetailSerializer
    lookup_field = 'slug'

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class PollsCompletedListView(ListAPIView):
    """
    Отображает пройденные пользователем опросы
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PollListSerializer

    def get_queryset(self):
        self.queryset = Poll.objects.filter(
            questions__answers__user=self.request.user
        ).order_by('start_date').distinct()
        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            queryset = queryset.all()
        return queryset


class PollCompletedRetrieveView(RetrieveAPIView):
    """
    Отображает детали о пройденном пользователем опросе
    """
    permission_classes = [IsAuthenticated]
    queryset = Poll.objects.all()
    serializer_class = PollResultSerializer
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        queryset = {
            'poll': instance,
            'answers': Answer.objects.filter(
                Q(user=request.user) & Q(question__poll=instance)
            ).order_by('complete_time', 'question__number')
        }
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)


class PollPassView(APIView):
    """
    Обрабатывает заполненную форму опроса
    """

    def post(self, request, slug):

        anonymous = request.data.get('anonymous', False)
        if request.user.id is None:
            anonymous = True

        poll = get_object_or_404(Poll, slug=slug)

        for i, answer_data in enumerate(request.data.get('answers', [])):

            number = answer_data.get('number')
            if number != i + 1:
                ValidationError('Question numbers must go in order and without spaces')
            question = get_object_or_404(Question, poll=poll, number=number)

            answer, chosen_answers = validate_and_create_answer_form(answer_data, question)

            if answer is None:
                return Response(status=400)

            if not anonymous:
                answer.user = request.user
            answer.save()

            if chosen_answers is not None:
                answer.chosen_answers.set(chosen_answers)
                answer.save()

        return Response(status=201)
