from django.urls import path
from .views import CarrinhoView, CheckoutView, PedidoLojistaListView, PedidoLojistaStatusView, MetodoPagamentoListCreateView, MetodoPagamentoDestroyView

urlpatterns = [
    # Rota: /api/carrinho/
    path('carrinho/', CarrinhoView.as_view(), name='meu_carrinho'),
    
    # Rota para finalizar a compra:
    path('checkout/', CheckoutView.as_view(), name='checkout_pedido'),

    # Rotas do Lojista (UC09)
    path('pedidos/', PedidoLojistaListView.as_view(), name='lojista_listar_pedidos'),
    path('pedidos/<int:pk>/status/', PedidoLojistaStatusView.as_view(), name='lojista_atualizar_status'),

    # Rotas de Pagamento (UC10)
    path('payments/', MetodoPagamentoListCreateView.as_view(), name='listar_criar_pagamentos'),
    path('payments/<int:pk>/', MetodoPagamentoDestroyView.as_view(), name='apagar_pagamento'),
]