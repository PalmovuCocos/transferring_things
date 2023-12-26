from django.urls import path
from django.views.decorators.cache import cache_page
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r'announcements', AnnouncementViewSet, basename='announcements')
print(router.urls)

urlpatterns = [
    path('api/announcements/',
         AnnouncementViewSet.as_view({'get': 'list'}),
         name='announcements'),

    path('api/announcements/<int:pk>',
         AnnouncementViewSet.as_view({'get': 'retrieve',
                                      'put': 'update',
                                      'delete': 'destroy'}),
         name='announcement_retrieve'),


    #path('api/announcements/', cache_page(60*5)(AnnouncementAPIView.as_view())),
    #path('api/announcements/<int:pk>/', AnnouncementRUDAPIView.as_view()),

    path('api/categories/', CategoryAPIView.as_view()),
    path('api/categories/announcements/', AnnouncementCategoryAPIView.as_view()),
    #path('api/categories/announcements/<int:pk>', AnnouncementRUDAPIView.as_view()),


    path('api/announcement/comments/', CommentAPIView.as_view()),

    path('api/announcement/comments/<int:pk>/', CommentRUDAPIView.as_view()),

    path('api/announcement/application/', ApplicationAPIView.as_view()),
    path('api/announcement/confirm_application/<int:pk>/',
         ConfirmApplicationAPIView.as_view()),
]
