from django.urls import path
from . import views

urlpatterns = [
    path('teste/', views.teste, name='teste'),  # Adicione o caminho para a view de teste
    path('ConfigIntegraWeb/', views.index_ConfigIntegraWeb, name='index_ConfigIntegraWeb'),  # Adicione o caminho para a view de configuração
    path('ConfigIntegraWeb/filtros', views.filtros_ConfigIntegraWeb, name='filtros_ConfigIntegraWeb'),  # Adicione o caminho para a view de filtros
    path('ConfigIntegraWeb/add_filtro', views.add_filtro_ConfigIntegraWeb, name='add_filtro_ConfigIntegraWeb'),  # Adicione o caminho para a view de adicionar filtro
    path('ConfigIntegraWeb/deletar_alterar_filtro', views.delete_alterar_filtro_ConfigIntegraWeb, name='deletar_alterar_filtro_ConfigIntegraWeb'),  # Adicione o caminho para a view de remover filtro
    path('ConfigIntegraWeb/admin', views.adminConfig_ConfigIntegraWeb, name='admin_ConfigIntegraWeb'),  # Adicione o caminho para a view de alterar filtro
    path('ConfigIntegraWeb/testar', views.testar_filtro_ConfigIntegraWeb, name='testar_ConfigIntegraWeb'),  # Adicione o caminho para a view de alterar filtro
]


