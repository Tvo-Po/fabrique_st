import datetime

from django.db.models import Q, QuerySet
from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import Poll
from .pagination import StandardResultsSetPagination
from .serializers import PollListSerializer, PollDetailSerializer


class PollsCurrentListView(ListAPIView):
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
    queryset = Poll.objects.all()
    serializer_class = PollDetailSerializer
    lookup_field = 'slug'
