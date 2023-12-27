from django.contrib import admin
from .models import Announcement, Category, Application, Comment

admin.site.site_header = 'Доска объявлений'


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    # список полей выводящихся при добавлении записей
    fields = ['announcer', 'category', 'name_thing', 'description']
    list_display = ('id',
                    'announcer', 'category', 'name_thing',
                    'description', 'photo')
    list_display_links = ('id', 'name_thing')
    search_fields = ['category__category_name', 'name_thing']
    list_per_page = 10
    ordering = ('category', 'name_thing')
    list_filter = ('category', 'announcer')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'applicant', 'comment')
    list_display_links = ('id', 'applicant')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'commentator', 'content', 'like', 'dislike', 'brief_info')
    list_per_page = 5

    @admin.display(description='Длинна комментария')
    def brief_info(self, comment: Comment):
        return len(comment.content)


