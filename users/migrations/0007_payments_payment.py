# Generated by Django 5.0.6 on 2024-07-05 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_remove_payments_payment_payments_payment_link_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='payments',
            name='payment',
            field=models.FloatField(blank=True, null=True, verbose_name='Сумма оплаты'),
        ),
    ]
