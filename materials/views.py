from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer, CourseDetailSerializer
from users.permissions import Moderator, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели Course
    """
    queryset = Course.objects.all()

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
            self.permission_classes = (~Moderator | IsAuthenticated,)
        elif self.action == ['update', 'retrieve']:
            self.permission_classes = [Moderator | IsOwner]
        elif self.action == 'destroy':
            self.permission_classes = (~Moderator | IsOwner,)
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
    permission_classes = [IsAuthenticated, IsOwner | Moderator]

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
    permission_classes = (IsAuthenticated, ~Moderator | IsOwner,)

