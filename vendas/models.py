from django.db import models
from django.conf import settings
from produtos.models import Produto

class Carrinho(models.Model):
    # OneToOneField garante que cada usuário tenha apenas UM carrinho ativo por vez
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carrinho')
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carrinho de {self.usuario.email}"

class ItemCarrinho(models.Model):
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    
    # A quantidade tem que ser no mínimo 1
    quantidade = models.PositiveIntegerField(default=1)

    def subtotal(self):
        # Uma função simples para calcular Quantidade * Preço na hora de retornar os dados
        return self.produto.preco * self.quantidade

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome}"

# Opções de status que o Lojista poderá atualizar depois
STATUS_CHOICES = (
    ('Pendente', 'Pendente'),
    ('Pago', 'Pago'),
    ('Enviado', 'Enviado'),
    ('Entregue', 'Entregue'),
    ('Cancelado', 'Cancelado'),
)

class Pedido(models.Model):
    # Um usuário pode ter vários pedidos ao longo do tempo (ForeignKey)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pedidos')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pendente')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario.email} ({self.status})"


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    
    # ATENÇÃO AQUI: on_delete=models.SET_NULL. 
    # Se o lojista apagar o produto da loja, o item do pedido não é deletado, apenas fica como "null".
    produto = models.ForeignKey(Produto, on_delete=models.SET_NULL, null=True)
    
    quantidade = models.PositiveIntegerField()
    # Este é o "Congelamento de Preço". Ele salva o preço exato do momento da compra.
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.preco_unitario * self.quantidade

    def __str__(self):
        nome_produto = self.produto.nome if self.produto else "Produto Removido da Loja"
        return f"{self.quantidade}x {nome_produto}"
    
class MetodoPagamento(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='metodos_pagamento')
    nome_titular = models.CharField(max_length=100)
    bandeira = models.CharField(max_length=20) # Ex: Visa, Mastercard
    
    # Isso guarda APENAS os últimos 4 dígitos para proteger o dado sensível, segundo as normas de segurança
    ultimos_digitos = models.CharField(max_length=4) 
    
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bandeira} terminado em {self.ultimos_digitos} - {self.usuario.email}"