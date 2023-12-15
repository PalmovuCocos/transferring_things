from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

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


class CreateCategoryAPIView(generics.ListCreateAPIView):
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


class RetrieveAnnouncementAPI(generics.RetrieveUpdateDestroyAPIView):
    """
    Вывод одной записи Announcement.
    Если пользователь - создатель записи, то можно изменять и удалять
    """
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = (IsCurrentUserOrReadOnly,)


class CommentAPIView(generics.ListCreateAPIView):
    """
    Вывод всех комментариев для отдельного объявления (или для всех)
    и создание комментариев для отдельного объявления
    """
    queryset = Comment.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = CommentSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CommentFilter

    def create(self, request, *args, **kwargs):
        print(self.kwargs)
        request.data['commentator'] = self.request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class RetrieveCommentAPI(generics.RetrieveUpdateDestroyAPIView):
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
    """
    queryset = Application.objects.all()
    permission_classes = (IsCurrentUser,)
    serializer_class = ApplicationSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ApplicationFilter

    def create(self, request, *args, **kwargs):
        request.data['applicant'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)


# class CreateApplicationAPIView(APIView):
#     """
#     создание нового заявления
#     """
#     serializer_class = ApplicationSerializer
#
#     def post(self, request, pk_ann):
#         new_application = Application.objects.create(
#             comment=request.data['comment'],
#             ad_id=pk_ann,
#             applicant_id=request.user.id)
#         return Response({'post': ApplicationSerializer(new_application).data})


class ConfirmApplicationAPIView(generics.UpdateAPIView):
    """
    изменение статуса заявления создателем объявления
    """
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = (IsCurrentUser,)

    def perform_update(self, serializer):
        serializer.save()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'update': ApplicationSerializer(instance).data})

        else:
            return Response({"message": "failed", "details": serializer.errors})


class RegisterAPI(generics.GenericAPIView):
    """
    Регистрация пользователя
    """
    serializer_class = RegisterSerializer

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        })
