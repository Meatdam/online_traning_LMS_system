# Generated by Django 5.0.6 on 2024-06-18 12:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0002_rename_curse_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='curse',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='materials.course', verbose_name='курс обучения'),
        ),
    ]
