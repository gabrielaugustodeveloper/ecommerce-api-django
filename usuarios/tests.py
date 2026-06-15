from rest_framework.test import APITestCase
from rest_framework import status
from .models import Usuario

class AutenticacaoTests(APITestCase):
    
    def setUp(self):
        """
        O setUp roda antes de CADA teste. 
        Usei para preparar os dados e as URLs simuladas.
        """
        # Substitua '/auth/register/' pela URL exata de cadastro da sua API
        self.url_registro = 'http://127.0.0.1:8000/auth/register/' 
        
        self.dados_usuario = {
            'username': 'teste_augusto',
            'email': 'teste@eject.com.br',
            'password': 'senha_super_segura_123',
            'is_lojista': False
        }

    def test_cadastro_usuario_sucesso(self):
        """ ✅ Garante que a API cria um usuário corretamente com status 201 """
        
        # O self.client simula um usuário enviando um JSON via POST
        response = self.client.post(self.url_registro, self.dados_usuario)

        #print("\n--- DETALHE DE ERRO 400 ---", response.data)
        
        # 1. A API deve retornar 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # 2. O banco de dados deve ter exatamente 1 usuário salvo
        self.assertEqual(Usuario.objects.count(), 1)
        # 3. O email salvo deve ser exatamente o como enviado
        self.assertEqual(Usuario.objects.get().email, 'teste@eject.com.br')

    def test_cadastro_email_duplicado_falha(self):
        """ ❌ Garante que o sistema bloqueia e-mails repetidos com status 400 """
        
        # 1º Passo: Cadastra o usuário pela primeira vez (vai dar certo)
        self.client.post(self.url_registro, self.dados_usuario)
        
        # 2º Passo: Tenta cadastrar EXATAMENTE o mesmo JSON de novo
        response = self.client.post(self.url_registro, self.dados_usuario)
        
        # A API deve interceptar e retornar 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # O banco de dados deve continuar tendo APENAS 1 usuário, provando que bloqueou
        self.assertEqual(Usuario.objects.count(), 1)