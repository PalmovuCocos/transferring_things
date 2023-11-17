from django.contrib import admin
from .models import Announcement, Category, Application, Comment


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('id', 'announcer', 'category', 'name_thing', 'description', 'photo')
    list_display_links = ('id', 'name_thing')
    search_fields = ('category', 'name_thing')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name')


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'applicant', 'comment')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'commentator', 'content', 'like', 'dislike')


admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(Comment, CommentAdmin)
