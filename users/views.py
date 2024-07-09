from datetime import datetime

import pytz
from django.views.generic import DetailView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import generics
from rest_framework.permissions import AllowAny

from base.settings import TIME_ZONE
from materials.models import Course, Lesson
from users.models import User, Payments
from users.serializers import UserSerializer, PaymentsSerializer
from users.services import create_stripe_product, create_stripe_price, create_stripe_session, checkout_session


class UserListApiView(generics.ListAPIView):
    """
    API для получения списка пользователей
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserCreateApiView(generics.CreateAPIView):
    """
    API для регистрации пользователя
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.last_login = datetime.now(pytz.timezone(TIME_ZONE))
        user.save()


class UserRetrieveApiView(generics.RetrieveAPIView):
    """
    API для получения пользователя
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserUpdateAPIView(generics.UpdateAPIView):
    """
    API для изменения пользователя
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class UserDestroyAPIView(generics.DestroyAPIView):
    """
    API для удаления пользователя
    """
    queryset = User.objects.all()


class PaymentsListAPIView(generics.ListAPIView):
    """
    API для получения списка оплаты
    """
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'payment_method')
    ordering_fields = ('payment_date',)


class PaymentsCreateAPIView(generics.CreateAPIView):
    """
    Payment create endpoint.
    """
    serializer_class = PaymentsSerializer

    def perform_create(self, serializer):
        """
        Привязывает платеж (с использованием stripe) к пользователю.
        """
        instance = serializer.save()
        instance.user = self.request.user

        course_id = self.request.data.get('course')
        lesson_id = self.request.data.get('lesson')
        if course_id:
            course_product = create_stripe_product(Course.objects.get(pk=course_id).name)
            course_price = create_stripe_price(instance.course.amount, course_product)
            session_id, payment_link = create_stripe_session(course_price, instance.pk)
        else:
            lesson_product = create_stripe_product(Lesson.objects.get(pk=lesson_id).name)
            lesson_price = create_stripe_price(instance.lesson.amount, lesson_product)
            session_id, payment_link = create_stripe_session(lesson_price, instance.pk)

        payment_status = checkout_session(session_id)
        instance.payment_status = payment_status
        instance.session_id = session_id
        instance.payment_link = payment_link
        instance.save()


class PaymentDetailView(DetailView):
    """
    Предтавление об оплате
    """
    model = Payments
