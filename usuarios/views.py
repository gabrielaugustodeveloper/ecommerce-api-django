from rest_framework import generics
from .serializers import UsuarioSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    # AllowAny permite que qualquer pessoa, mesmo sem estar logada, acesse essa rota para se cadastrar
    permission_classes = (AllowAny,)
    serializer_class = UsuarioSerializer

class SolicitarResetSenhaView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            # Gera um token seguro e temporário do próprio Django
            token = PasswordResetTokenGenerator().make_token(user)
            # Codifica o ID do usuário para colocar na URL
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Monta o link que o usuário teoricamente clicaria no e-mail
            link = f"http://127.0.0.1:8000/auth/reset-password/{uid}/{token}/"
            
            # "Envia" o e-mail (vai aparecer no terminal)
            send_mail(
                'Recuperação de Senha - New Style',
                f'Olá! Clique no link para resetar sua senha: {link}',
                'noreply@newstyle.com',
                [email],
                fail_silently=False,
            )
            return Response({"message": "E-mail de recuperação enviado com sucesso."}, status=status.HTTP_200_OK)
            
        except User.DoesNotExist:
            # Por segurança, se retorna com sucesso mesmo se o e-mail não existir para evitar vazamento de dados de clientes reais
            return Response({"message": "Se o e-mail estiver cadastrado, um link foi enviado."}, status=status.HTTP_200_OK)


class ResetarSenhaView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        try:
            # Descodifica o ID do usuário que veio na URL
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        # Verifica se o usuário existe e se o token é válido/não expirou
        if user is not None and PasswordResetTokenGenerator().check_token(user, token):
            nova_senha = request.data.get('password')
            user.set_password(nova_senha) # Criptografa a nova senha
            user.save()
            return Response({"message": "Senha alterada com sucesso!"}, status=status.HTTP_200_OK)
            
        return Response({"error": "Token inválido ou expirado."}, status=status.HTTP_400_BAD_REQUEST)
    
class ContatoView(APIView):
    # Qualquer pessoa pode aceder a esta rota, sem precisar de Token
    permission_classes = [AllowAny]

    def post(self, request):
        nome = request.data.get('nome')
        email = request.data.get('email')
        mensagem = request.data.get('mensagem')

        # Validação simples
        if not nome or not email or not mensagem:
            return Response(
                {"error": "Por favor, preencha o nome, email e mensagem."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Construção da mensagem
        assunto = f"Novo Contato da Loja - {nome}"
        corpo_email = f"Nome: {nome}\nEmail do Cliente: {email}\n\nMensagem:\n{mensagem}"
        
        # Envio do e-mail
        send_mail(
            assunto,
            corpo_email,
            'sistema@newstyle.com', # O e-mail que envia (remetente automático)
            ['admin@newstyle.com'], # O e-mail do lojista que vai receber
            fail_silently=False,
        )

        return Response({"message": "A sua mensagem foi enviada com sucesso!"}, status=status.HTTP_200_OK)