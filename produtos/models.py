from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Produto(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.PositiveIntegerField() # Positive garante que não fique negativo
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='produtos')
    ativo = models.BooleanField(default=True) # Campo para controle de exibição

    def __str__(self):
        return self.nome
    
class Variacao(models.Model):
    # Relaciona a variação a um produto específico
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='variacoes')
    
    # Ex: P, M, G, GG ou 38, 40, 42
    tamanho = models.CharField(max_length=50, blank=True, null=True)
    
    # Ex: Azul, Preto, Branco
    cor = models.CharField(max_length=50, blank=True, null=True)
    
    # O estoque agora vive aqui >:)
    estoque = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.produto.nome} - {self.tamanho} | {self.cor}"