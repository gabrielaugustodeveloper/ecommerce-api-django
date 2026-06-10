from rest_framework import permissions

class IsLojistaOrReadOnly(permissions.BasePermission):
    """
    Permite acesso de leitura a qualquer usuário (mesmo não logado).
    Mas permite criação, edição e exclusão APENAS para usuários com is_lojista=True.
    """
    def has_permission(self, request, view):
        # SAFE_METHODS são os métodos de apenas leitura: GET, HEAD ou OPTIONS.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Se não for leitura (ou seja, for POST, PUT, PATCH, DELETE), 
        # o usuário precisa estar logado E ter is_lojista igual a True.
        return bool(
            request.user and 
            request.user.is_authenticated and 
            request.user.is_lojista
        )