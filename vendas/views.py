from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.shortcuts import get_object_or_404
from .models import Carrinho, ItemCarrinho, Pedido, ItemPedido, MetodoPagamento
from produtos.models import Produto
from .serializers import CarrinhoSerializer, PedidoSerializer, MetodoPagamentoSerializer
from .permissions import IsLojista
from django.db import transaction # Importante para a prevenção de falhas

class CarrinhoView(APIView):
    # Apenas usuários logados podem ter um carrinho
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # get_or_create busca o carrinho do usuário. Se não existir, ele cria automaticamente!
        carrinho, created = Carrinho.objects.get_or_create(usuario=request.user)
        serializer = CarrinhoSerializer(carrinho)
        return Response(serializer.data)

    def post(self, request):
        carrinho, created = Carrinho.objects.get_or_create(usuario=request.user)
        
        # Pega os dados que o cliente enviou no JSON
        produto_id = request.data.get('produto')
        quantidade = int(request.data.get('quantidade', 1))

        # Verifica se o produto realmente existe no banco de dados
        produto = get_object_or_404(Produto, id=produto_id)

        # Busca se esse item já está no carrinho. Se não estiver, cria.
        item, item_created = ItemCarrinho.objects.get_or_create(
            carrinho=carrinho, 
            produto=produto,
            defaults={'quantidade': quantidade}
        )

        # Se o item já existia no carrinho, a gente só soma a quantidade nova
        if not item_created:
            item.quantidade += quantidade
            item.save()

        serializer = CarrinhoSerializer(carrinho)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    # O decorator atomic garante que o bloco inteiro é uma transação segura
    @transaction.atomic 
    def post(self, request):
        carrinho = get_object_or_404(Carrinho, usuario=request.user)
        itens_carrinho = carrinho.itens.all()

        # Prevenção 1: O carrinho não pode estar vazio
        if not itens_carrinho.exists():
            return Response({"error": "O seu carrinho está vazio."}, status=status.HTTP_400_BAD_REQUEST)

        # 1. Cria o Pedido inicial (ainda sem total)
        pedido = Pedido.objects.create(usuario=request.user, total=0)
        total_pedido = 0

        # 2. Percorre os itens do carrinho para os transferir
        for item in itens_carrinho:
            # Prevenção 2: Verificar se há stock suficiente para concluir a venda
            if item.produto.estoque < item.quantidade:
                # Se falhar aqui, o @transaction.atomic anula a criação do pedido automaticamente!
                return Response(
                    {"error": f"Stock insuficiente para o produto '{item.produto.nome}'."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 3. Desconta do stock da loja e guarda a alteração
            item.produto.estoque -= item.quantidade
            item.produto.save()

            # 4. Transfere para o ItemPedido congelando o preço atual
            ItemPedido.objects.create(
                pedido=pedido,
                produto=item.produto,
                quantidade=item.quantidade,
                preco_unitario=item.produto.preco
            )
            
            # Soma ao total da compra
            total_pedido += (item.produto.preco * item.quantidade)

        # 5. Atualiza o valor final do pedido
        pedido.total = total_pedido
        pedido.save()

        # 6. Esvazia o carrinho do utilizador (apaga os itens)
        itens_carrinho.delete()

        # Devolve o recibo (Pedido) com Status 201 Created
        serializer = PedidoSerializer(pedido)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
# 1. View para Listar os Pedidos (GET)
class PedidoLojistaListView(generics.ListAPIView):
    serializer_class = PedidoSerializer
    permission_classes = [IsLojista]

    def get_queryset(self):
        # A regra de negócio exige os mais antigos primeiro (order_by('criado_em'))
        queryset = Pedido.objects.all().order_by('criado_em')
        
        # Permite filtrar pelo URL, ex: /api/pedidos/?status=Pendente
        status_param = self.request.query_params.get('status', None)
        if status_param:
            queryset = queryset.filter(status=status_param)
            
        return queryset

# 2. View para Atualizar o Status (PATCH)
class PedidoLojistaStatusView(APIView):
    permission_classes = [IsLojista]

    def patch(self, request, pk):
        pedido = get_object_or_404(Pedido, pk=pk)
        novo_status = request.data.get('status')

        if not novo_status:
            return Response({"error": "É obrigatório enviar o novo status."}, status=status.HTTP_400_BAD_REQUEST)

        # Regra de negócio: Dicionário de transições válidas
        transicoes_validas = {
            'Pendente': ['Pago', 'Cancelado'],
            'Pago':     ['Enviado', 'Cancelado'],
            'Enviado':  ['Entregue'],
            'Entregue': [], # Fim da linha
            'Cancelado':[]  # Fim da linha
        }

        # Verifica se o novo status está na lista de movimentos permitidos para o status atual
        movimentos_permitidos = transicoes_validas.get(pedido.status, [])
        
        if novo_status not in movimentos_permitidos:
            return Response(
                {"error": f"Transição inválida. Um pedido '{pedido.status}' não pode mudar para '{novo_status}'."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Se passou na validação, atualiza e guarda
        pedido.status = novo_status
        pedido.save()

        serializer = PedidoSerializer(pedido)
        return Response(serializer.data, status=status.HTTP_200_OK)

class MetodoPagamentoListCreateView(generics.ListCreateAPIView):
    serializer_class = MetodoPagamentoSerializer
    permission_classes = [IsAuthenticated] # Qualquer utilizador logado pode ter cartões

    def get_queryset(self):
        # REGRA CRÍTICA: Filtra a base de dados para mostrar apenas os métodos deste utilizador
        return MetodoPagamento.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        # Quando criar, associa automaticamente o cartão ao utilizador do Token JWT
        serializer.save(usuario=self.request.user)


class MetodoPagamentoDestroyView(generics.DestroyAPIView):
    serializer_class = MetodoPagamentoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Garante que um utilizador não consegue apagar o cartão de outro, mesmo que adivinhe o ID
        return MetodoPagamento.objects.filter(usuario=self.request.user)