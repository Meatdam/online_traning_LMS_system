from rest_framework.serializers import ModelSerializer

from users.models import User, Payments


class UserSerializer(ModelSerializer):
    """
    Сериализатор для модели User
    """
    class Meta:
        model = User
        fields = '__all__'


class PaymentsSerializer(ModelSerializer):
    """
    Сериализатор для модели Payments
    """
    class Meta:
        model = Payments
        fields = '__all__'
