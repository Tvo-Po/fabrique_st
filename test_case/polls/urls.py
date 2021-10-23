from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView,
                                            TokenVerifyView)

from .views import (PollsCurrentListView, PollRetrieveView,
                    PollAdminCreateView, PollAdminEditView,
                    PollsCompletedListView, PollPassView,
                    PollCompletedRetrieveView)


urlpatterns = [
    path('polls/', PollsCurrentListView.as_view()),
    path('polls/<slug:slug>', PollRetrieveView.as_view()),
    path('polls/<slug:slug>/pass', PollPassView.as_view()),
    path('polls-admin/', PollAdminCreateView.as_view()),
    path('polls-admin/<slug:slug>', PollAdminEditView.as_view()),
    path('passed-polls/', PollsCompletedListView.as_view()),
    path('passed-polls/<slug:slug>', PollCompletedRetrieveView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]