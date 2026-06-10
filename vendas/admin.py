from django.contrib import admin
from .models import Carrinho, ItemCarrinho, Pedido, ItemPedido, MetodoPagamento

admin.site.register(Carrinho)
admin.site.register(ItemCarrinho)
admin.site.register(ItemPedido)
admin.site.register(MetodoPagamento)

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'status')
    list_filter = ('status',)