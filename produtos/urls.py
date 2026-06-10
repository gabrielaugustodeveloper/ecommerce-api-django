from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoriaViewSet, ProdutoViewSet, VariacaoViewSet

# O Router cria automaticamente as rotas GET, POST, PUT, PATCH e DELETE
router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)
router.register(r'produtos', ProdutoViewSet, basename='produto') # O basename é necessário porque o queryset é dinâmico no ProdutoViewSet
router.register(r'variacoes', VariacaoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]