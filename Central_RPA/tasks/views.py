from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest #for Typing
from django.contrib.auth.decorators import permission_required, login_required
from django.views.decorators.cache import cache_page
from django.contrib.auth.models import User, Permission
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .Entities.tarefas import Tarefas
from .Entities.informativo_task import Informativo
from typing import List, Dict
from time import sleep
from . import models
from . import forms
import json
from datetime import datetime
import os

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

#@permission_required('tasks.tasks', raise_exception=True) #type: ignore   
@login_required()
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
    
    tarefas_validas.listar_tarefas()
    return redirect('tasks_index')

@login_required
@permission_required('tasks.pagamentos_diarios', raise_exception=True) #type: ignore
def pagamentos_diarios(request: WSGIRequest):
    tarefas:List[Tarefas] = []
    #permission_user = [x.codename for x in request.user.user_permissions.all()]#type: ignore  
    for permission in request.user.get_all_permissions(): #type: ignore
        for tarefa_valida in tarefas_validas.tarefas:
            if tarefa_valida.permission == permission:
                if 'Pagamentos Diarios' in tarefa_valida.nome_para_key:
                    tarefas += [tarefa_valida]
    
    #tarefas[0].
    task = tarefas[0]
    
    informativo_pgmt_diario_texts:list = []
    django_argv_path:str = ""
    try:
        infor:dict = json.loads(task.infor)
        if (informativo_pgmt_diario_path:=infor.get('informativo_pgmt_diario')):
            informativo_pgmt_diario_texts:list = Informativo(informativo_pgmt_diario_path).read()
        if (path:=infor.get('django_argv')):
            django_argv_path = path
    except json.JSONDecodeError as e:
        print(e)
    
    content:dict = {
        "tarefa": task,
        "informativo_pgmt_diario_texts" : reversed(informativo_pgmt_diario_texts),
        "informativo_pgmt_diario_path" : informativo_pgmt_diario_path,
        "django_argv_path": django_argv_path
    }
    return render(request, 'pagamento_diario.html', content)

@login_required
def retorno_informativo(request: WSGIRequest, path):
    try:
        texts = Informativo(path).read()
    except Exception as err:
        texts = []
    return JsonResponse(texts, safe=False)

@login_required
@permission_required('tasks.pagamentos_diarios', raise_exception=True) #type: ignore
def pagamentos_diarios_iniciar(request: WSGIRequest):
    if request.method == "POST":
        post = request.POST
        print(post)
        
        path_informativo = str(post.get('path_informativo'))
        if post.get(path_informativo):
            if os.path.exists(path_informativo):
                os.unlink(path_informativo)
        
        django_argv:dict ={
            "date" : post.get('data')
        }
        
        if post.get('boleto'):
            django_argv['boleto'] = True
        else:
            django_argv['boleto'] = False
            
        if post.get('consumo'):
            django_argv['consumo'] = True
        else:
            django_argv['consumo'] = False

        if post.get('imposto'):
            django_argv['imposto'] = True
        else:
            django_argv['imposto'] = False

        if post.get('darfs'):
            django_argv['darfs'] = True
        else:
            django_argv['darfs'] = False

        if post.get('relacionais'):
            django_argv['relacionais'] = True
        else:
            django_argv['relacionais'] = False

        path = str(post.get('path'))
        if os.path.exists(os.path.dirname(path)):
            with open(path, 'w', encoding='utf-8')as _file:
                json.dump(django_argv, _file)
            
                
            tarefas:List[Tarefas] = []
            #permission_user = [x.codename for x in request.user.user_permissions.all()]#type: ignore  
            for permission in request.user.get_all_permissions(): #type: ignore
                for tarefa_valida in tarefas_validas.tarefas:
                    if tarefa_valida.permission == permission:
                        if 'Pagamentos Diarios' in tarefa_valida.nome_para_key:
                            tarefas += [tarefa_valida]
            
            #tarefas[0].
            task = tarefas[0]
            task.executar()


        
    return redirect('pagamento_diario')
