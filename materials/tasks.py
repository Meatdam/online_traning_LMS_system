import smtplib
from datetime import datetime

import pytz
from dateutil.relativedelta import relativedelta
from django.core.mail import send_mail

from celery import shared_task

from base.settings import EMAIL_HOST_USER, TIME_ZONE
from materials.models import Course, Subscription
from users.models import User


@shared_task
def send_email(course_id):
    """
    Отправка сообщени об изменение курса
    """
    course = Course.objects.get(pk=course_id)

    subscriptions = Subscription.objects.filter(course=course, subscript=True)
    emails = list(subscriptions.values_list('user__email', flat=True))

    try:
        send_mail(f"Курс '{course.name}' обновился", 'Вы можете просмотреть изменения на сайте!',
                  EMAIL_HOST_USER, emails)
    except smtplib.SMTPException as e:
        raise print(f"Ошибка отправки сообщения {e}")


@shared_task
def user_deactivation():
    """
    Отправка письма с уведомлением о деактивации пользователя
    """
    current_date_time = datetime.now(pytz.timezone(TIME_ZONE))
    inactive = current_date_time - relativedelta(months=1)
    users = User.objects.filter(is_active=True, last_login__lte=inactive)
    users.update(is_active=False)
    try:
        send_mail(f"Уведомление о деактивации пользователя {users.email}",
                  'Ваш аккаунт был деактивирован.',
                  EMAIL_HOST_USER, [users.email])
    except smtplib.SMTPException as e:
        raise print(f"Ошибка отправки сообщения {e}")
