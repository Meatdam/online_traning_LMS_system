# Generated by Django 5.0.6 on 2024-06-19 14:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_payments_course_alter_payments_lesson_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payments',
            options={'ordering': ('-payment_date',), 'verbose_name': 'оплата', 'verbose_name_plural': 'оплаты'},
        ),
    ]