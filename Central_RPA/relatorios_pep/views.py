from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth.decorators import permission_required, login_required
from django.http import JsonResponse
from datetime import datetime
from Central_RPA.utils import Utils
import os
import json
from tasks.views import tarefas_validas, Tarefas
from . import models
from time import sleep
from .Entities.divi_from_sharepoint import DiviFromSharepoint

def get_tarefa(nome_tarefa:str) -> Tarefas|None:
    tarefas_validas.listar_tarefas()
    #print([tarefa.nome for tarefa in tarefas_validas.tarefas], nome_tarefa)
    for tarefa in tarefas_validas.tarefas:
        if tarefa.nome == nome_tarefa:
            return tarefa
    return None

@login_required
@permission_required('tasks.relatoriosPep', raise_exception=True)
def index(request: WSGIRequest):
    try:
        automation_path = models.AdminConfig.objects.get(argv="automation_path").value
    except:
        automation_path = ""
    try:
        automation = models.AdminConfig.objects.get(argv="automation").value
    except:
        automation = ""
    
    try:
        sharepoint_path = models.AdminConfig.objects.get(argv="sharepoint_path").value
    except:
        sharepoint_path = ""
    
    #print(get_tarefa(automation))
    try:
        divisoes = DiviFromSharepoint(sharepoint_path, datetime.now())
        divisoes = divisoes.get_lista_divisao("Obra em andamento")
    except:
        divisoes = []
    
    content = {
        "automation_path_value": automation_path,
        "automation_value": automation,
        "sharepoint_path": sharepoint_path,
        "divisoes": divisoes,
    }
    return render(request, 'index_relatoriosPep.html', content)


@login_required
@permission_required('tasks.relatoriosPep', raise_exception=True)
def start(request: WSGIRequest):
    if request.method == 'POST':
        post = request.POST
        #print(post)
        
        argvs = {}
        if (divisoes:=post.get('divisoes')):
            if divisoes:
                argvs["divisao"] = divisoes.split(',')
            else:
                return Utils.message_retorno(request, "Divisões não informadas", name_route="index_relatoriosPep")
        else:
            return Utils.message_retorno(request, "Divisões não informadas", name_route="index_relatoriosPep")
        
        if (date:=post.get('date')):
            argvs["date"] = datetime.strptime(date, '%Y-%m-%d').isoformat()
        else:
            return Utils.message_retorno(request, "Data não informada", name_route="index_relatoriosPep")
        
        if (final_date:=post.get('final_date')):
            argvs["final_date"] = datetime.strptime(final_date, '%Y-%m-%d').isoformat()
        else:
            argvs["final_date"] = None
            
        if (post.get('acumulado')):
            argvs["acumulado"] = True
        else:
            argvs["acumulado"] = False

        try:
            file_argvs_path = models.AdminConfig.objects.get(argv="automation_path").value
        except:
            file_argvs_path = ""

        if not os.path.exists(file_argvs_path):
            return Utils.message_retorno(request, "Pasta do Arquivo args não existe!", name_route="index_relatoriosPep")
        
        file_argvs_path = os.path.join(file_argvs_path, "args.json")
        with open(file_argvs_path, 'w') as file:
            file.write(json.dumps(argvs))
        
        try:
            tarefa = models.AdminConfig.objects.get(argv="automation").value
        except:
            tarefa = ""
            
        tarefa = get_tarefa(tarefa)
        if tarefa:
            tarefa.executar()
            #sleep(5)
            return Utils.message_retorno(request, "Relatório de PEP iniciado com sucesso!", name_route="index_relatoriosPep")
        else:
            return Utils.message_retorno(request, "Tarefa de automação não encontrada!", name_route="index_relatoriosPep")
                
    return redirect('index_relatoriosPep')
    

@login_required
@Utils.superUser_required
def adminConfig(request: WSGIRequest):
    if request.method == 'POST':
        post = request.POST
        #print(post)
        
        erros = ""
        if (automation_path:=post.get('automation_path')):
            if not os.path.exists(automation_path):
                automation_path = ""
                erros += "Error: Caminho de automação não existe!\n"
            models.AdminConfig.objects.update_or_create(argv="automation_path", defaults={"value": automation_path})
        else:
            erros += "Error: Caminho de automação não informado!\n"
            
        if (automation:=post.get('automation')):
            if get_tarefa(automation) is None:
                automation = ""
                erros += "Error: Tarefa de automação não existe!\n"
            else:
                models.AdminConfig.objects.update_or_create(argv="automation", defaults={"value": automation})
                
        if (sharepoint_path:=post.get('sharepoint_path')):
            if not os.path.exists(sharepoint_path):
                sharepoint_path = ""
                erros += "Error: Caminho do Sharepoint não existe!\n"
            models.AdminConfig.objects.update_or_create(argv="sharepoint_path", defaults={"value": sharepoint_path})
        else:
            erros += "Error: Caminho do Sharepoint não informado!\n"
        
        
        return Utils.message_retorno(request, (f"Configurações salvas com sucesso!" if not erros else erros), name_route="index_relatoriosPep")
    
    return redirect('index_relatoriosPep')

@login_required
@permission_required('tasks.relatoriosPep', raise_exception=True)
def statusTarefa(request: WSGIRequest):
    try:
        tarefa = models.AdminConfig.objects.get(argv="automation").value
    except:
        tarefa = ""
        
    tarefa = get_tarefa(tarefa)
    if tarefa:
        status = tarefa.status()

        return JsonResponse({"status": status})
    
    return JsonResponse({"status": "Error"})


@login_required
@permission_required('tasks.relatoriosPep', raise_exception=True)
def lista_downloads(request: WSGIRequest):
    try:
        automation_path = models.AdminConfig.objects.get(argv="automation_path").value
    except:
        automation_path = ""
        
    if os.path.exists(automation_path):
        download_path = os.path.join(automation_path, "fileZip")
        if os.path.exists(download_path):
            lista_files = []
            for file in os.listdir(download_path):
                file_path = os.path.join(download_path, file)
                if os.path.isfile(file_path):
                    date_file = os.path.getmtime(file_path)
                    lista_files.append({"name":file, "path":file_path, "date": datetime.fromtimestamp(date_file).strftime('%d/%m/%Y %H:%M:%S')})
            return JsonResponse(lista_files, safe=False)
    
    return JsonResponse([], safe=False)