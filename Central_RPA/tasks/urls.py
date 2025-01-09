from django.urls import path
from django.http import HttpResponse
from . import views



urlpatterns = [
    #path('registrar', endpoints.registro, name='Main'), #type: ignore
    #path('', views.filtro_lista, name='filtro'),
    #path('listar', views.lista, name="listar")
    path('', views.index, name='newTasks_index'),
    path('start_task/<str:nome_para_key>', views.start_task, name='start_task'),
    path('stop_task/<str:nome_para_key>', views.stop_task, name='stop_task'),
    path('status', views.status, name='status'),
    path('criar_tarefa', views.criar_tarefa, name='criar_tarefa'),
    path('deletar_tarefa/<int:pk>', views.deletar_tarefa, name='deletar_tarefa'),
    path('alter_form/<int:pk>', views.alterar_tarefa_form, name='alter_form_task'),
    path('alter/<int:pk>', views.alterar_tarefa, name='alter_task'),
    path('pagamento_diario/', views.pagamentos_diarios, name='pagamento_diario'),
    path('pagamentos_diarios_iniciar/', views.pagamentos_diarios_iniciar, name='pagamentos_diarios_iniciar'),
    path('retorno_informativo/<str:path>', views.retorno_informativo, name='retorno_informativo'),
    #############
    path('list_tasks/', views.list_tasks, name='list_tasks'),
    path('start_newTask', views.start_newTask, name='start_newTask'),
    path('old/', views.index_old, name='tasks_index'),
    
]

