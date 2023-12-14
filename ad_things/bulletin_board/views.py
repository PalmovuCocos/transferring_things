from rest_framework import generics
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

    # def perform_create(self, serializer):
    #     ad_id = self.kwargs['pk']
    #     print('aaa', self.request.data, ad_id, self.request.user.id, '\n\n', sep='\n')
    #     serializer.save(ad=ad_id,
    #                     commentator=self.request.user.id
    #                     )

    def post(self, request, pk):
        new_comment = Comment.objects.create(content=request.data['content'],
                                             ad_id=pk,
                                             commentator_id=request.user.id)
        return Response({'post': CommentSerializer(new_comment).data})


class RetrieveCommentAPI(generics.RetrieveUpdateDestroyAPIView):
    """
    вывод отдельного комментария, а также
    изменение и удаление если создатель комментария текущий пользователь
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsCurrentUserOrReadOnly,)


class ApplicationAPIView(generics.ListAPIView):
    """
    вывод списка заявлений у определенного объявления
    """
    queryset = Application.objects.all()
    permission_classes = (IsCurrentUser,)
    serializer_class = ApplicationSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ApplicationFilter


class CreateApplicationAPIView(APIView):
    """
    создание нового заявления
    """

    def post(self, request, pk_ann):
        new_application = Application.objects.create(comment=request.data['comment'],
                                                     ad_id=pk_ann,
                                                     applicant_id=request.user.id)
        return Response({'post': ApplicationSerializer(new_application).data})


class ConfirmApplicationAPIView(generics.UpdateAPIView):
    """
    изменение статуса заявления создателем объявления
    """
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = (IsCurrentUser,)

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
