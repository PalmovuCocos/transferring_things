from django.core.mail import send_mail
from rest_framework import generics, status
from rest_framework.response import Response

from .filters import AnnouncementCategoryFilter, CommentFilter, \
    ApplicationFilter
from .models import *
from .serializers import (AnnouncementSerializer,
                          CommentSerializer,
                          ApplicationSerializer,
                          CategorySerializer,
                          RegisterSerializer,
                          UserSerializer)

from .permissions import (IsAuthenticatedOrReadOnly,
                          IsCurrentUser,
                          IsCurrentUserOrReadOnly)

from django_filters import rest_framework as filters


class AnnouncementAPIView(generics.ListCreateAPIView):
    """
    Вывод всех объявлений и создание объявления
    """
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class AnnouncementRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Вывод одной записи Announcement.
    Если пользователь - создатель записи, то можно изменять и удалять
    """
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = (IsCurrentUserOrReadOnly,)


class CategoryAPIView(generics.ListCreateAPIView):
    """
    Вывод и создание категорий для авторизированных пользователей
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )


class AnnouncementCategoryAPIView(generics.ListAPIView):
    """
    Вывод всех объявлений по категориям (записывать в поисковой строке),
    если пользователь авторизован, то можно создавать новые с данной категорией
    """
    queryset = Announcement.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = AnnouncementSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AnnouncementCategoryFilter


class CommentAPIView(generics.ListCreateAPIView):
    """
    Вывод всех комментариев для отдельного объявления (или для всех)
    и создание новых комментариев
    """
    queryset = Comment.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = CommentSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CommentFilter

    def perform_create(self, serializer):
        recipient = Announcement.objects.get(pk=self.request.data["ad"])
        send_mail(
            "Доска объявлений",
            f'Под Вашим объявлением {self.request.data["ad"]} '
            f'был оставлен комментарий',
            "",
            [recipient.announcer.email],
            fail_silently=False,
        )
        serializer.save()


class CommentRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    вывод отдельного комментария, а также
    изменение и удаление если создатель комментария текущий пользователь
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsCurrentUserOrReadOnly,)


class ApplicationAPIView(generics.ListCreateAPIView):
    """
    вывод списка заявлений у определенного объявления
    и добавление нового объявления
    """
    queryset = Application.objects.all()
    permission_classes = (IsCurrentUser,)
    serializer_class = ApplicationSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ApplicationFilter

    def perform_create(self, serializer):
        recipient = Announcement.objects.get(pk=self.request.data["ad"])
        send_mail(
            "Доска объявлений",
            f'На Ваше объявление {self.request.data["ad"]} '
            f'откликнулись!',
            "",
            [recipient.announcer.email],
            fail_silently=False,
        )
        serializer.save()


class ConfirmApplicationAPIView(generics.UpdateAPIView):
    """
    изменение статуса заявления создателем объявления
    """
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = (IsCurrentUser,)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data={"response": True},
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response({'update': ApplicationSerializer(instance).data})

        else:
            return Response({"message": "failed", "details": serializer.errors})


class RegisterAPI(generics.CreateAPIView):
    serializer_class = RegisterSerializer

