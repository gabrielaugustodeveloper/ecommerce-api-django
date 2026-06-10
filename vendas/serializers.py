from rest_framework import serializers
from .models import Carrinho, ItemCarrinho, Pedido, ItemPedido, MetodoPagamento

class ItemCarrinhoSerializer(serializers.ModelSerializer):
    # Traz o nome do produto para facilitar a visualização
    produto_nome = serializers.ReadOnlyField(source='produto.nome')
    # Chama a função subtotal que criamos no models.py
    subtotal = serializers.ReadOnlyField() 

    class Meta:
        model = ItemCarrinho
        fields = ['id', 'produto', 'produto_nome', 'quantidade', 'subtotal']

class CarrinhoSerializer(serializers.ModelSerializer):
    itens = ItemCarrinhoSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Carrinho
        fields = ['id', 'criado_em', 'itens', 'total']

    # Calcula o total somando o subtotal de todos os itens
    def get_total(self, obj):
        return sum(item.subtotal() for item in obj.itens.all())
    
class ItemPedidoSerializer(serializers.ModelSerializer):
    produto_nome = serializers.ReadOnlyField(source='produto.nome')
    subtotal = serializers.ReadOnlyField()

    class Meta:
        model = ItemPedido
        fields = ['id', 'produto', 'produto_nome', 'quantidade', 'preco_unitario', 'subtotal']

class PedidoSerializer(serializers.ModelSerializer):
    itens = ItemPedidoSerializer(many=True, read_only=True)

    class Meta:
        model = Pedido
        fields = ['id', 'status', 'total', 'criado_em', 'itens']

class MetodoPagamentoSerializer(serializers.ModelSerializer):
    # O utilizador envia o número completo, mas nós nunca o devolvemos num GET
    numero_cartao = serializers.CharField(write_only=True, max_length=16, min_length=13)

    class Meta:
        model = MetodoPagamento
        # O campo 'numero_cartao' entra aqui para o POST, e o 'ultimos_digitos' para o GET
        fields = ['id', 'nome_titular', 'bandeira', 'numero_cartao', 'ultimos_digitos', 'criado_em']
        read_only_fields = ['ultimos_digitos', 'criado_em']

    def create(self, validated_data):
        # Remove o número completo dos dados validados
        numero_cartao = validated_data.pop('numero_cartao')
        
        # Extraí apenas os últimos 4 dígitos e guarda-os no campo 'ultimos_digitos'
        validated_data['ultimos_digitos'] = numero_cartao[-4:]
        
        return super().create(validated_data)