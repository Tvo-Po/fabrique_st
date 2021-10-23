from django.urls import path

from test_case.polls.views import PollsCurrentListView, PollRetrieveView

urlpatterns = [
    path('polls/', PollsCurrentListView.as_view()),
    path('polls/<slug:slug>', PollRetrieveView.as_view()),
]