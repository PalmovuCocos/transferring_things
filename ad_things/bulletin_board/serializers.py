from rest_framework import serializers
from .models import Announcement, Category, Application, Comment


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
    # commentator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = "__all__"



