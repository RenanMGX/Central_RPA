from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest #for Typing
from django.contrib.auth.decorators import permission_required, login_required
from django.views.decorators.cache import cache_page
from django.contrib.auth.models import User, Permission
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .Entities.tarefas import Tarefas
from typing import List, Dict
from time import sleep
from . import models
from . import forms
import asyncio

class TarefasValidas:
    tarefas = []
    
    def listar_tarefas(self) -> List[Tarefas]:  
        self.tarefas = [Tarefas(pk=x.pk,nome_tarefa=x.tarefa, permission=x.permission, can_stop=x.can_stop, infor=str(x.infor)) for x in models.Tarefas.objects.all()]
        return self.tarefas

tarefas_validas = TarefasValidas()
tarefas_validas.listar_tarefas()
        
@login_required()
@permission_required('tasks.tasks', raise_exception=True) #type: ignore   
def index(request:WSGIRequest, ):    
    tarefas:List[Tarefas] = []
    #permission_user = [x.codename for x in request.user.user_permissions.all()]#type: ignore  
    for permission in request.user.get_all_permissions(): #type: ignore
        for tarefa_valida in tarefas_validas.tarefas:
            if tarefa_valida.permission == permission:
                tarefas += [tarefa_valida]

   
    content:dict = {
        'tarefas': tarefas,
        'user': request.user,
        'atualizar_status_auto': True, #<--------- alterar
        'all_permissions': Permission.objects.all()
    }
    
    return render(request, 'tasks.html', content)

@login_required()
@permission_required('tasks.tasks', raise_exception=True) #type: ignore   
def status(request: WSGIRequest):
    return JsonResponse(Tarefas.all_status())

@login_required()
@permission_required('tasks.tasks', raise_exception=True) #type: ignore   
def start_task(request: WSGIRequest, permission): 
    if request.method == "GET":
        for tarefa_perm in tarefas_validas.tarefas:
            if tarefa_perm.permission == permission:
                if tarefa_perm.permission in request.user.get_all_permissions(): #type: ignore   
                    tarefa_perm.executar()
                    return redirect('tasks_index')
    
    return redirect('tasks_index')


@login_required()
@permission_required('tasks.tasks', raise_exception=True) #type: ignore   
def stop_task(request: WSGIRequest, permission): 
    if request.method == "GET":
        for tarefa_perm in tarefas_validas.tarefas:
            if tarefa_perm.permission == permission:
                if tarefa_perm.permission in request.user.get_all_permissions(): #type: ignore   
                    tarefa_perm.encerrar()
                    return redirect('tasks_index')
    
    return redirect('tasks_index')


@login_required()
@permission_required('admin.add_logentry', raise_exception=True) #type: ignore  
def criar_tarefa(request: WSGIRequest):
    if request.method == "POST":
        form = forms.TarefasForm(request.POST)
        if form.is_valid():
            form.save()
    
    tarefas_validas.listar_tarefas()
    return redirect('tasks_index')

@login_required()
@permission_required('admin.add_logentry', raise_exception=True) #type: ignore
def deletar_tarefa(request: WSGIRequest, pk):
    if request.method == "GET":
        item = get_object_or_404(models.Tarefas, pk=pk)
        if item:
            item.delete()
    
    return redirect('tasks_index')