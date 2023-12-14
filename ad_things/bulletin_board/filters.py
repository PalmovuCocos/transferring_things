from django_filters.rest_framework import filters, FilterSet

from .models import (Announcement)


class AnnouncementCategoryFilter(FilterSet):
    category = filters.CharFilter()
    announcer = filters.CharFilter()

    class Meta:
        model = Announcement
        fields = ['category', 'announcer']
