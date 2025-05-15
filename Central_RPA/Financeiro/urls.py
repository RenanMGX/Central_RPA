from django.urls import path
from . import views

urlpatterns = [
    path('test', views.test, name='test'),
    path('index_relatAberturaDesp', views.index_relatAberturaDesp, name='index_relatAberturaDesp'),
    path('upFiles_relatAberturaDesp', views.upFiles_relatAberturaDesp, name='upFiles_relatAberturaDesp'),
    path('adminConfig_relatAberturaDesp', views.adminConfig_relatAberturaDesp, name='adminConfig_relatAberturaDesp'),
    path('status_relatAberturaDesp', views.tarefa_status_relatAberturaDesp, name='status_relatAberturaDesp'),
    path('listaTarefas_relatAberturaDesp', views.lista_files_relatAberturaDesp, name='listaTarefas_relatAberturaDesp'),
    path('logs_relatAberturaDesp', views.log_relatAberturaDesp, name='log_relatAberturaDesp'),
    path('index_cadastrarVtax', views.index_cadastrarVtax, name='index_cadastrarVtax'),
    path('adminConfig_cadastrarVtax', views.adminConfig_cadastroVtax, name='adminConfig_cadastrarVtax'),
]
