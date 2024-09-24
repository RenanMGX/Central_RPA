from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest #for Typing
from django.contrib.auth.decorators import permission_required, login_required
from django.views.decorators.cache import cache_page
from django.contrib.auth.models import User, Permission
from django.http import JsonResponse
from .Entities.tarefas import Tarefas
from typing import List, Dict

tarefas_validas:Dict[str, object] = {
    'tasks.pagamentos_diarios': Tarefas("Automações\\testes")
}

@login_required()
@permission_required('tasks.tasks', raise_exception=True) #type: ignore   
def index(request:WSGIRequest):    
    tarefas = []
    permission_user = [x.codename for x in request.user.user_permissions.all()]#type: ignore  
    for permission in permission_user:
        if tarefas_validas.get(permission):
            tarefas.append(tarefas_validas.get(permission))
    
    content:dict = {
        'tarefas': tarefas,
        'user': request.user
    }
    
    return render(request, 'tasks.html', content)

@login_required()
@permission_required('tasks.tasks', raise_exception=True) #type: ignore   
def execute(request: WSGIRequest, nome_tarefa):
    print(nome_tarefa)
    print(request.method)
    if request.method == "GET":
        Tarefas.executar(nome_tarefa)
    return redirect('index')

@login_required()
@permission_required('tasks.tasks', raise_exception=True) #type: ignore   
def status(request: WSGIRequest, nome_tarefa):
    content:dict = {
        'tarefa': Tarefas(nome_tarefa).status(),
    }
    return JsonResponse(content)