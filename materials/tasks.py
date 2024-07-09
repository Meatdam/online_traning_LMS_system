import smtplib
from datetime import datetime

import pytz
from dateutil.relativedelta import relativedelta
from django.core.mail import send_mail

from celery import shared_task

from base.settings import EMAIL_HOST_USER, TIME_ZONE
from materials.models import Course
from users.models import User


@shared_task
def send_email(user):
    """
    Отправка письма с уведомлением об изменении курса
    """
    course = Course.objects.filter(pk=user).first()
    email_list = []

    if course:
        subscription = course.subscription_set.filter(subscript=True)
        for subscript in subscription:
            email_list.append(subscript.user.email)

    if len(email_list) > 0:
        try:
            send_mail(f"Курс '{course.name}' обновился", 'Вы можете просмотреть изменения на сайте!',
                      EMAIL_HOST_USER, [*email_list])
        except smtplib.SMTPException as e:
            raise print(f"Ошибка отправки сообщения {e}")


@shared_task
def user_deactivation():
    """
    Отправка письма с уведомлением о деактивации пользователя
    """
    users = User.objects.filter(is_active=True)
    today = datetime.now(pytz.timezone(TIME_ZONE))

    for user in users:
        login = user.last_login
        login_active = login + relativedelta(months=1)
        if today > login_active and not user.is_superuser:
            user.is_active = False
            user.save()
            try:
                send_mail(f"Уведомление о деактивации пользователя {user.email}",
                          'Ваш аккаунт был деактивирован.',
                          EMAIL_HOST_USER, [user.email])
            except smtplib.SMTPException as e:
                raise print(f"Ошибка отправки сообщения {e}")
