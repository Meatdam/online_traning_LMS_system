from rest_framework import viewsets, generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from materials.models import Course, Lesson, Subscription
from materials.paginators import MaterialsPaginator
from materials.serializers import CourseSerializer, LessonSerializer, CourseDetailSerializer, SubscriptionSerializer
from users.permissions import Moderator, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели Course
    """
    queryset = Course.objects.all()
    pagination_class = MaterialsPaginator

    def perform_create(self, serializer):
        """
        Перед сохранением курса добавляем владельца
        """
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseSerializer

    def get_queryset(self):
        """
        Получаем список курсов в зависимости от прав пользователя
        """
        if Moderator().has_permission(self.request, self):
            return Course.objects.all()
        else:
            return Course.objects.filter(owner=self.request.user)

    def get_permissions(self):
        """
        Пермишены в зависимости от действия
        """
        if self.action == 'create':
            self.permission_classes = (~Moderator, IsAuthenticated,)
        elif self.action == ['update', 'retrieve']:
            self.permission_classes = [IsAuthenticated, Moderator | IsOwner]
        elif self.action == 'destroy':
            self.permission_classes = (IsAuthenticated, IsOwner,)
        return super().get_permissions()


class LessonCreateAPIView(generics.CreateAPIView):
    """
    API для создания нового урока
    """
    serializer_class = LessonSerializer
    permission_classes = [~Moderator, IsAuthenticated]

    def perform_create(self, serializer):
        """
        Перед сохранением урока добавляем владельца
        """
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(generics.ListAPIView):
    """
    API для получения списка уроков
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = MaterialsPaginator

    def get_queryset(self):
        """
        Получаем список уроков в зависимости от прав пользователя
        """
        if Moderator().has_permission(self.request, self):
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """
    API для получения урока
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, Moderator | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """
    API для изменения урока
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, Moderator | IsOwner,)


class LessonDestroyAPIView(generics.DestroyAPIView):
    """
    API для удаления урока
    """
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsOwner,)


class SubscriptionApiView(APIView):
    """
    API для подписки на курс
    """
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def post(self, *args, **kwargs):
        """
        Создание подписки на курс
        """
        user = self.request.user
        course_id = self.request.data.get('course')
        course_item = get_object_or_404(Course, pk=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'

        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'подписка добавлена'

        return Response({"message": message})


