import datetime

from django.db.models import Q, QuerySet
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, GenericAPIView
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAdminUser

from .models import Poll
from .pagination import StandardResultsSetPagination
from .serializers import PollListSerializer, PollDetailSerializer


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
