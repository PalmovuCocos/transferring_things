from django.urls import path

from bulletin_board.views import AnnouncementAPIView

urlpatterns = [
    path('api/v1/announcement', AnnouncementAPIView.as_view()),
]