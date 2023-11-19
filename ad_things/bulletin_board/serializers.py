from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Announcement, Category, Application, Comment
from django.core.mail import send_mail


class AnnouncementSerializer(serializers.ModelSerializer):
    announcer = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Announcement
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ApplicationSerializer(serializers.ModelSerializer):
    # applicant = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Application
        fields = "__all__"

    def partial_update(self, instance, validated_data):
        # instance.applicant = validated_data.get("applicant", instance.applicant)
        # instance.ad = validated_data.get("ad", instance.ad)
        # instance.comment = validated_data.get("comment", instance.comment)

        instance.response = validated_data.get("response", instance.response)
        instance.save()
        return instance


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = "__all__"


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name')
        extra_kwargs = {
            'password': {'write_only': True},
            }

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'],
                                        password=validated_data['password'],
                                        first_name=validated_data['first_name'],
                                        last_name=validated_data['last_name'])
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

