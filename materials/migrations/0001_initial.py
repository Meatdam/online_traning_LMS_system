# Generated by Django 5.0.6 on 2024-06-18 11:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Curse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='название курса')),
                ('image', models.ImageField(blank=True, null=True, upload_to='curse', verbose_name='Превью')),
                ('description', models.TextField(blank=True, null=True, verbose_name='описание курса')),
            ],
            options={
                'verbose_name': 'курс обучения',
                'verbose_name_plural': 'курсы обучения',
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='название')),
                ('description', models.TextField(blank=True, null=True, verbose_name='описание')),
                ('image', models.ImageField(blank=True, null=True, upload_to='lesson', verbose_name='Превью')),
                ('url', models.URLField(blank=True, null=True, verbose_name='ссылка на видео')),
                ('curse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materials.curse', verbose_name='курс обучения')),
            ],
            options={
                'verbose_name': 'урок',
                'verbose_name_plural': 'уроки',
            },
        ),
    ]
