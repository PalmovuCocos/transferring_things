from django.contrib import admin
from .models import Announcement, Category, Application, Comment


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('id', 'announcer', 'category', 'name_thing', 'description', 'photo')
    list_display_links = ('id', 'name_thing')
    search_fields = ('category', 'name_thing')


admin.site.register(Announcement, AnnouncementAdmin)
