from rest_framework.permissions import BasePermission


class IsUserOrStaff(BasePermission):
    """
    Пермишен для пользователей и админов
    """
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return request.user == view.get_object().id


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

