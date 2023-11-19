from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import AnnouncementSerializer, CommentSerializer, ApplicationSerializer, CategorySerializer
from .permissions import IsAuthenticatedOrReadOnly, IsCurrentUser, IsCurrentUserOrReadOnly, IsNotOwnerUser


class AnnouncementAPIView(generics.ListCreateAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class CategoryAPIView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, category):
        queryset = Announcement.objects.filter(category=category)
        serializer = AnnouncementSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        post_new = Category.objects.create(category_name=request.data['category_name'])
        return Response({'post': CategorySerializer(post_new).data})


# Вывод одной записи Announcement. Если пользователь - создатель записи, то можно изменять и удалять
class RetrieveAnnouncementAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = (IsCurrentUserOrReadOnly,)


# для вывода ВСЕХ коментариев отдельного объявления и создания для данного объявления
class CommentAPIView(APIView):
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


# вывод отдельного комментария. Если создатель комментария, то + изменение, удаление
class RetrieveCommentAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsCurrentUserOrReadOnly,)


# вывод списка заявлений у определенного объявления
class ApplicationAPIView(APIView):
    permission_classes = (IsCurrentUser,)

    def get(self, request, pk_ann):
        queryset = Application.objects.filter(ad_id=pk_ann)
        serializer = ApplicationSerializer(queryset, many=True)
        return Response(serializer.data)


# создание нового заявления
class CreateApplicationAPIView(APIView):

    def post(self, request, pk_ann):
        new_application = Application.objects.create(comment=request.data['comment'],
                                                     ad_id=pk_ann,
                                                     applicant_id=request.user.id)
        return Response({'post': ApplicationSerializer(new_application).data})


# изменение статуса заявления создателем объявления
class ConfirmApplicationAPIView(generics.UpdateAPIView):
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

