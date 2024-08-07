from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):
    """
    Тестирование создания, изменения и получения урока
    """
    def setUp(self):
        self.user = User.objects.create(email="test@mail.ru")
        self.course = Course.objects.create(name="test1", description="test1", owner=self.user)
        self.lesson = Lesson.objects.create(name="test2", description="test2_2", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_create(self):
        url = reverse('materials:lesson_create')
        data = {
            "name": "Java",
            "description": "good lesson",
            "course": self.course.pk
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        url = reverse('materials:lesson_update', args=(self.lesson.pk,))
        data = {
            "name": "Java + ",
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('name', ), "Java + ", )

    def test_lesson_retrieve(self):
        url = reverse('materials:lesson_detail', args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('name', 'description'), "test2", "test2_2")

    def test_lesson_delete(self):
        url = reverse('materials:lesson_delete', args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse('materials:lesson_list')
        response = self.client.get(url)
        data = response.json()
        result = {'count': 1,
                  'next': None,
                  'previous': None,
                  'results': [
                      {'id': self.lesson.id,
                       'name': self.lesson.name,
                       'description': self.lesson.description,
                       'image': None,
                       'url': self.lesson.url,
                       'course': self.lesson.course,
                       'owner': self.lesson.owner.id}
                  ]}
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class CourseTestCase(APITestCase):
    """
    Тест кейс Course
    """
    def setUp(self):
        self.user = User.objects.create(email="test_1@mail.ru")
        self.course = Course.objects.create(name="testCourse", description="Course_test", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_course_create(self):
        url = reverse('materials:course-list')
        data = {
            "name": "Python",
            "description": "good course",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.all().count(), 2)

    def test_course_update(self):
        url = reverse('materials:course-detail', args=(self.course.pk,))
        data = {
            "name": "Java + ",
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('name', ), "Java + ", )

    def test_course_retrieve(self):
        url = reverse('materials:course-detail', args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('name', 'description'), "testCourse", "Course_test")

    def test_course_delete(self):
        url = reverse('materials:course-detail', args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_course_list(self):
        url = reverse('materials:course-list')
        response = self.client.get(url)
        data = response.json()
        result = {'count': 1,
                  'next': None,
                  'previous': None,
                  'results': [
                      {'id': self.course.pk,
                       'lesson_count': response.json()['results'][0]['lesson_count'],
                       'lesson': [],
                       'subscription': False,
                       'name': 'testCourse',
                       'image': None,
                       'description': 'Course_test',
                       'owner': self.course.owner.id}]}

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class SubscriptionTestCase(APITestCase):
    """
    Тест кейс Subscription
    """

    def setUp(self):
        self.user = User.objects.create(email="test_2@mail.ru")
        self.course = Course.objects.create(name="testCourse", description="Course_test", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subscription(self):
        url = reverse('materials:subscription_create')
        data = {
            "course": self.course.pk
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Subscription.objects.all().count(), 1)
        self.assertEqual(response.json(), {"message": "подписка добавлена"})

    def test_unsubscription(self):
        url = reverse('materials:subscription_create')
        data = {
            "course": self.course.pk
        }
        self.client.post(url, data)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Subscription.objects.all().count(), 0)
        self.assertEqual(response.json(), {"message": "подписка удалена"})
