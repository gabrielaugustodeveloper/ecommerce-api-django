from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, SolicitarResetSenhaView, ResetarSenhaView, ContatoView

urlpatterns = [
    # Rota de Cadastro: POST /auth/register/
    path('register/', RegisterView.as_view(), name='auth_register'),
    
    # Rota de Login (Gera o Token JWT): POST /auth/login/
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # Rota opcional para renovar o token caso ele expire
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Rotas de senha
    path('password-reset/', SolicitarResetSenhaView.as_view(), name='password_reset'),
    path('reset-password/<str:uidb64>/<str:token>/', ResetarSenhaView.as_view(), name='password_reset_confirm'),

    # Rota de contato (UC06):
    path('contato/', ContatoView.as_view(), name='contato_loja'),
]