from rest_framework import viewsets, filters
from .models import Categoria, Produto, Variacao
from .serializers import CategoriaSerializer, ProdutoSerializer, VariacaoSerializer
from .permissions import IsLojistaOrReadOnly # Importando a permissão customizada

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    # Adicionando a permissão customizada para categorias também:
    permission_classes = [IsLojistaOrReadOnly]

class ProdutoViewSet(viewsets.ModelViewSet):
    serializer_class = ProdutoSerializer
    permission_classes = [IsLojistaOrReadOnly]
    
    # Habilita os motores de busca e ordenação do DRF
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    
    # Define em quais campos o usuário pode pesquisar (ex: ?search=astronauta)
    search_fields = ['nome', 'descricao', 'categoria__nome']
    
    # Define por quais campos ele pode ordenar (ex: ?ordering=preco)
    ordering_fields = ['preco', 'nome']

    def get_queryset(self):
        """
        Refatoração da query: 
        - Lojistas podem ver todos os produtos (para poderem editar os inativos).
        - Clientes comuns só podem ver os produtos que estão com ativo=True.
        """
        user = self.request.user
        if user.is_authenticated and getattr(user, 'is_lojista', False):
            return Produto.objects.all()
        
        # Filtra apenas os ativos para o público geral
        return Produto.objects.filter(ativo=True)

class VariacaoViewSet(viewsets.ModelViewSet):
    queryset = Variacao.objects.all()
    serializer_class = VariacaoSerializer
    # A mesma permissão do produto: Lojista edita, Cliente só lê
    permission_classes = [IsLojistaOrReadOnly]