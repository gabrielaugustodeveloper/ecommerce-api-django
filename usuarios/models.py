from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    # Garante que o e-mail seja único no banco de dados
    email = models.EmailField(unique=True)

    # Campo adicionado para diferenciar os papéis de Cliente e Lojista
    is_lojista = models.BooleanField(default=False)

    # Dizendo ao Django para usar o e-mail como campo principal de login
    USERNAME_FIELD = 'email'
    
    # O username continuará existindo, mas será preenchido automaticamente ou secundário
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email