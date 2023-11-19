from django.urls import path

from bulletin_board.views import *

urlpatterns = [
    path('api/announcement', AnnouncementAPIView.as_view()),
    path('api/announcement_category/<int:category>/', CategoryAPIView.as_view()),

    path('api/announcement/<int:pk>', RetrieveAnnouncementAPI.as_view()),

    path('api/announcement_comment/<int:pk>', CommentAPIView.as_view()),

    path('api/retrieve_comment/<int:pk>', RetrieveCommentAPI.as_view()),

    path('api/application/<int:pk_ann>', ApplicationAPIView.as_view()),
    path('api/create_application/<int:pk_ann>', CreateApplicationAPIView.as_view()),
    path('api/confirm_application/<int:pk>', ConfirmApplicationAPIView.as_view()),
]

