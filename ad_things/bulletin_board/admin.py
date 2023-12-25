from django.contrib import admin
from .models import Announcement, Category, Application, Comment

admin.site.site_header = 'Доска объявлений'


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'announcer', 'category', 'name_thing', 'description', 'photo')
    list_display_links = ('id', 'name_thing')
    search_fields = ('category', 'name_thing')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'applicant', 'comment')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'commentator', 'content', 'like', 'dislike')
