from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import AnnouncementSerializer, CommentSerializer, ApplicationSerializer, CategorySerializer, \
    RegisterSerializer, UserSerializer
from .permissions import IsAuthenticatedOrReadOnly, IsCurrentUser, IsCurrentUserOrReadOnly


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
    Вывод всех объявлений по категориям,
    если пользователь авторизован, то можно создавать новые с данной категорией
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = AnnouncementSerializer

    def get(self, request, category):
        queryset = Announcement.objects.filter(category=category)
        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(serializer.data)


class RetrieveAnnouncementAPI(generics.RetrieveUpdateDestroyAPIView):
    """
    Вывод одной записи Announcement.
    Если пользователь - создатель записи, то можно изменять и удалять
    """
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = (IsCurrentUserOrReadOnly,)


class CommentAPIView(APIView):
    """
    Вывод всех комментариев и создание комментариев для отдельного объявления
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, pk):
        queryset = Comment.objects.filter(ad=pk)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

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


class ApplicationAPIView(APIView):
    """
    вывод списка заявлений у определенного объявления
    """
    permission_classes = (IsCurrentUser,)

    def get(self, request, pk_ann):
        queryset = Application.objects.filter(ad_id=pk_ann)
        serializer = ApplicationSerializer(queryset, many=True)
        return Response(serializer.data)


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


