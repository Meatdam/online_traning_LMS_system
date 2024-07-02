from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


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



