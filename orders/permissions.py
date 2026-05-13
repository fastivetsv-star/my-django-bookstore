from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешает просматривать данные всем пользователям.
    Но создавать, редактировать или удалять может только Администратор.
    """
    def has_permission(self, request, view):
        
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return bool(request.user and request.user.is_staff)

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешает редактировать объект только его владельцу (создателю).
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.customer == request.user