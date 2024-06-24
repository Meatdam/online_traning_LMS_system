from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


from users.models import User, Payments
from users.permissions import IsUserOrStaff
from users.serializers import UserSerializer, PaymentsSerializer


class UserListApiView(generics.ListAPIView):
    """
    API для получения списка пользователей
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserCreateApiView(generics.CreateAPIView):
    """
    API для регистрации пользователя
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserRetrieveApiView(generics.RetrieveAPIView):
    """
    API для получения пользователя
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserUpdateAPIView(generics.UpdateAPIView):
    """
    API для изменения пользователя
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsUserOrStaff]


class UserDestroyAPIView(generics.DestroyAPIView):
    """
    API для удаления пользователя
    """
    queryset = User.objects.all()
    permission_classes = [IsUserOrStaff]


class PaymentsListAPIView(generics.ListAPIView):
    """
    API для получения списка уроков
    """
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'payment_method')
    ordering_fields = ('payment_date',)
