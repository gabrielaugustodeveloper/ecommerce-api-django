from rest_framework import serializers
from .models import Categoria, Produto, Variacao

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__' # Retorna todos os campos (id e nome)

class VariacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variacao
        fields = ['id', 'produto', 'tamanho', 'cor', 'estoque']

class ProdutoSerializer(serializers.ModelSerializer):
    # O many=True e read_only=True garantem que a lista de variações venha embutida no produto
    variacoes = VariacaoSerializer(many=True, read_only=True)

    class Meta:
        model = Produto
        fields = ['id', 'nome', 'descricao', 'preco', 'estoque', 'categoria', 'ativo', 'variacoes']
