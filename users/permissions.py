from rest_framework.permissions import BasePermission


class Moderator(BasePermission):
    """
    Пермишен для модераторов
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name='manager').exists()


class IsOwner(BasePermission):
    """
    Пермишен для владельца лекций и курсов
    """
    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False
