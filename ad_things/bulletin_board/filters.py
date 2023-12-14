from django_filters.rest_framework import filters, FilterSet

from .models import (Announcement, Comment, Application)


class AnnouncementCategoryFilter(FilterSet):
    category = filters.CharFilter()
    announcer = filters.CharFilter()

    class Meta:
        model = Announcement
        fields = ['category', 'announcer']


class CommentFilter(FilterSet):
    ad = filters.CharFilter()

    class Meta:
        model = Comment
        fields = ['ad']


class ApplicationFilter(FilterSet):
    ad = filters.CharFilter()

    class Meta:
        model = Application
        fields = ['ad']
