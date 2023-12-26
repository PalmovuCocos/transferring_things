from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    path('api/announcements/', cache_page(60*5)(AnnouncementAPIView.as_view())),
    path('api/announcements/<int:pk>/', AnnouncementRUDAPIView.as_view()),

    path('api/categories/', CategoryAPIView.as_view()),
    path('api/categories/announcements/', AnnouncementCategoryAPIView.as_view()),
    path('api/categories/announcements/<int:pk>', AnnouncementRUDAPIView.as_view()),


    path('api/announcement/comments/', CommentAPIView.as_view()),

    path('api/announcement/comments/<int:pk>/', CommentRUDAPIView.as_view()),

    path('api/announcement/application/', ApplicationAPIView.as_view()),
    path('api/announcement/confirm_application/<int:pk>/',
         ConfirmApplicationAPIView.as_view()),
]
