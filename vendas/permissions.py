from rest_framework import permissions

class IsLojista(permissions.BasePermission):
    """
    Permite o acesso EXCLUSIVAMENTE a utilizadores autenticados que tenham is_lojista=True.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_lojista)