# Generated by Django 4.2.7 on 2023-11-18 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bulletin_board', '0002_alter_announcement_options_alter_application_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='response',
            field=models.BooleanField(default=False, verbose_name='Отклик'),
        ),
    ]
