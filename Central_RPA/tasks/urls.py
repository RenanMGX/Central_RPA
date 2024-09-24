from django.urls import path
from django.http import HttpResponse
from . import views



urlpatterns = [
    #path('registrar', endpoints.registro, name='Main'), #type: ignore
    #path('', views.filtro_lista, name='filtro'),
    #path('listar', views.lista, name="listar")
    path('', views.index, name='tasks_index'),
    path('executar/<str:nome_tarefa>', views.execute, name='executar'),
    path('status/<str:nome_tarefa>', views.status, name='status'),
]

