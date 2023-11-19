from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    category_name = models.CharField(max_length=30, verbose_name='Название категории')

    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'


class Announcement(models.Model):
    announcer = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Объявитель')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория')
    name_thing = models.CharField(max_length=30, verbose_name='Название вещи')
    description = models.TextField(max_length=180, verbose_name='Описание')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name='Фото')

    class Meta:
        verbose_name_plural = 'Объявления'
        verbose_name = 'Объявление'


class Application(models.Model):
    applicant = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Заявитель')
    ad = models.ForeignKey(Announcement, on_delete=models.PROTECT, verbose_name='Объявление')
    comment = models.TextField(max_length=180, verbose_name='Комментарий')
    response = models.BooleanField(default=False, verbose_name='Отклик')

    class Meta:
        verbose_name_plural = 'Заявки'
        verbose_name = 'Заявка'


class Comment(models.Model):
    commentator = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Комментатор')
    ad = models.ForeignKey(Announcement, on_delete=models.PROTECT, verbose_name='Объявление')
    content = models.TextField(max_length=120, verbose_name='Содержимое')
    like = models.PositiveIntegerField(verbose_name='Нравится', default=0)
    dislike = models.PositiveIntegerField(verbose_name='Не нравится', default=0)

    class Meta:
        verbose_name_plural = 'Комментарии'
        verbose_name = 'Комментарий'
