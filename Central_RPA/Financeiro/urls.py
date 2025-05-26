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
    path('start_cadastrarVtax', views.start_cadastrarVtax, name='start_cadastrarVtax'),
    path('retorno_cadastrarVtax', views.retorno_cadastrarVtax, name='retorno_cadastrarVtax'),
    
    path('index_renegociarDividas', views.index_renegociarDividas, name='index_renegociarDividas'),
    path('adminConfig_renegociarDividas', views.adminConfig_renegociarDividas, name='adminConfig_renegociarDividas'),
    path('upFiles_renegociarDividas', views.upFiles_renegociarDividas, name='upFiles_renegociarDividas'),
    path('status_renegociarDividas', views.status_renegociarDividas, name='status_renegociarDividas'),

    

]
