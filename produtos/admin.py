from django.contrib import admin
from .models import Categoria, Produto, Variacao

admin.site.register(Categoria)
admin.site.register(Variacao)

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    # Escolha de quais colunas aparecerão na tabela do admin
    list_display = ('nome', 'preco', 'estoque', 'ativo')
    # Adiciona uma barra de pesquisa
    search_fields = ('nome',)
    # Adiciona filtros laterais
    list_filter = ('ativo', 'categoria')

