from django.urls import path

from .views import *

urlpatterns = [
    path('api/announcement/', AnnouncementAPIView.as_view()),
    path('api/announcement_category/', AnnouncementCategoryAPIView.as_view()),
    path('api/category/', CreateCategoryAPIView.as_view()),

    path('api/retrieve_announcement/<int:pk>/', RetrieveAnnouncementAPI.as_view()),

    path('api/announcement_comment/', CommentAPIView.as_view()),

    path('api/retrieve_comment/<int:pk>/', RetrieveCommentAPI.as_view()),

    path('api/application/<int:pk_ann>/', ApplicationAPIView.as_view()),
    path('api/create_application/<int:pk_ann>/', CreateApplicationAPIView.as_view()),
    path('api/confirm_application/<int:pk>/', ConfirmApplicationAPIView.as_view()),
]

