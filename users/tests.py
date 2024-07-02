from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from users.models import User, Payments


class TestUser(APITestCase):
    """
        Тестирование создание пользователя
    """
    def setUp(self):
        self.user = User.objects.create(email='admin@test.com')
        self.client.force_authenticate(user=self.user)

    def test_create_user(self):

        data = {
            "email": "test@example.com",
            "password": 1234
        }
        response = self.client.post(
            '/users/create/', data=data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.json(),
            {'id': response.json()['id'],
             "password": response.json()['password'],
             "email": "test@example.com", "city": None,
             "first_name": "", 'date_joined': response.json()['date_joined'],
             "groups": [],
             "image": None,
             "is_active": True,
             "is_staff": False,
             "is_superuser": False,
             "last_login": None,
             "last_name": "",
             "phone": None,
             "user_permissions": []})

        self.assertTrue(User.objects.all().count() == 2)


class PaymentTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@bk.ru', password=12345)
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(owner=self.user, name='курс', description='описание курса')
        self.lesson = Lesson.objects.create(owner=self.user, name='урок', description='описание урока',
                                            url='https://youtube.com/', course=self.course)
        self.payment = Payments.objects.create(user=self.user,
                                               course=self.course, lesson=self.lesson, payment=2000,
                                               payment_method='cash')

    def test_payment_list(self):
        """
        Тест на получение списка платежей.
        """
        url = reverse('users:payments_list')
        response = self.client.get(url)
        data = response.json()
        result = [
            {
                'id': self.payment.pk,
                'payment_date': data[0]['payment_date'],
                'payment': self.payment.payment,
                'payment_method': self.payment.payment_method,
                'user': self.user.pk,
                'course': self.course.pk,
                'lesson': self.lesson.pk
            }
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)
