from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth.decorators import login_required, permission_required
from . import models
from Central_RPA.utils import Utils
from tasks.views import start_task, tarefas_validas
from django.http import JsonResponse
from .Entities.log_informativo import LogInformativo
from datetime import datetime
from django.http import HttpResponse, Http404
import os
from time import sleep
from copy import deepcopy


def test(request: WSGIRequest):
    return JsonResponse({"status": "ok"})

@login_required
@Utils.superUser_required
def testar_automacao(request: WSGIRequest):
    tarefas_validas.listar_tarefas()
    try:
        name_automation = models.CaminhoAutomacao.objects.get(pk=1).nome
    except models.CaminhoAutomacao.DoesNotExist:
        name_automation = ""
    
    if request.method == 'GET':
        start_task(request=request, nome_para_key=name_automation)
        return Utils.message_retorno(request, 'Teste iniciado com sucesso', 'index_consolidarDadosMultiplasPlanilhas')
    
    return redirect('index_consolidarDadosMultiplasPlanilhas')

@login_required         
@permission_required('tasks.consolidarDadosMultiplasPlanilhas', raise_exception=True)
def index(request: WSGIRequest):
    #start_task(request=request, nome_para_key=r'Automações\\testes')
    #print([x.nome_para_key for x in tarefas_validas.listar_tarefas()])
    try:
        upload_path = models.Uploadpath.objects.get(pk=1).path
    except models.Uploadpath.DoesNotExist:
        upload_path = f'C:\\Users\\{os.getlogin()}\\Downloads'
    
    tarefas_validas.listar_tarefas()   
    try:
        name_automation = models.CaminhoAutomacao.objects.get(pk=1).nome
    except models.CaminhoAutomacao.DoesNotExist:
        name_automation = ""
       
    #start_task(request=request, nome_para_key=name_automation) 
        
    infomativo:list = LogInformativo(path=os.path.join(upload_path, 'informativoLog.json')).load()
    infomativo.reverse()

    content = {
        'upload_path': upload_path,
        'informativo': infomativo,
        'name_automation': name_automation
    }
    return render(request, 'consolidarDadosMultiplasPlanilhas_index.html', content)

@login_required
@permission_required('tasks.consolidarDadosMultiplasPlanilhas', raise_exception=True)
def upload(request: WSGIRequest):
    try:
        upload_path = models.Uploadpath.objects.get(pk=1).path
    except models.Uploadpath.DoesNotExist:
        upload_path = f'C:\\Users\\{os.getlogin()}\\Downloads'
    
    tarefas_validas.listar_tarefas()   
    try:
        name_automation = models.CaminhoAutomacao.objects.get(pk=1).nome
    except models.CaminhoAutomacao.DoesNotExist:
        name_automation = ""
        
    upload_path = os.path.join(upload_path, 'Files')
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
        
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        for file in files:
            if file.name.lower().endswith(('xls', 'xlsx', 'xlsm')):
                file_path = os.path.join(upload_path, file.name)
                with open(file_path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
        if files:
            request.method = 'GET'
            start_task(request=request, nome_para_key=name_automation)
            return Utils.message_retorno(request, 'Arquivos enviados com sucesso', 'index_consolidarDadosMultiplasPlanilhas')
    
    
    return redirect('index_consolidarDadosMultiplasPlanilhas')

@login_required
@Utils.superUser_required
def set_upload_path(request: WSGIRequest):
    if request.method == 'POST':
        if (path:=request.POST.get('path')):
            if not os.path.exists(path):
                return Utils.message_retorno(request, 'Caminho não existe', 'index_consolidarDadosMultiplasPlanilhas')
               
            try:
                upload_path = models.Uploadpath.objects.get(pk=1)
                upload_path.path = path
                upload_path.save()
            except models.Uploadpath.DoesNotExist:
                upload_path = models.Uploadpath(path=path)
                upload_path.save()
            
            return Utils.message_retorno(request, 'Caminho alterado com sucesso', 'index_consolidarDadosMultiplasPlanilhas')
               
    return redirect('index_consolidarDadosMultiplasPlanilhas')

@login_required
@Utils.superUser_required
def set_name_automation(request: WSGIRequest):
    if request.method == 'POST':
        if (name:=request.POST.get('name')):
            name = name.strip()
            if not name in [x.nome_para_key for x in tarefas_validas.listar_tarefas()]:
                return Utils.message_retorno(request, 'Nome da automação não existe', 'index_consolidarDadosMultiplasPlanilhas')
            
            try:
                name_automation = models.CaminhoAutomacao.objects.get(pk=1)
                name_automation.nome = name
                name_automation.save()
            except models.CaminhoAutomacao.DoesNotExist:
                name_automation = models.CaminhoAutomacao(nome=name)
                name_automation.save()
            
            return Utils.message_retorno(request, 'Nome da automação alterado com sucesso', 'index_consolidarDadosMultiplasPlanilhas')
               
    return redirect('index_consolidarDadosMultiplasPlanilhas')


@login_required
@permission_required('tasks.consolidarDadosMultiplasPlanilhas', raise_exception=True)
def log_informativo(request: WSGIRequest):
    try:
        upload_path = models.Uploadpath.objects.get(pk=1).path
    except models.Uploadpath.DoesNotExist:
        upload_path = f'C:\\Users\\{os.getlogin()}\\Downloads'
    
    infomativo:list = LogInformativo(path=os.path.join(upload_path, 'informativoLog.json')).load()
    infomativo.reverse()
    
    return JsonResponse(infomativo, safe=False)
    
@login_required
@permission_required('tasks.consolidarDadosMultiplasPlanilhas', raise_exception=True)
def file_to_download_path(request: WSGIRequest):
    try:
        upload_path = models.Uploadpath.objects.get(pk=1).path
    except models.Uploadpath.DoesNotExist:
        upload_path = f'C:\\Users\\{os.getlogin()}\\Downloads'
    
    file_to_download_path = os.path.join(upload_path, 'ReturnFiles')
    if os.path.exists(file_to_download_path):
        files_path = [os.path.join(file_to_download_path, x) for x in os.listdir(file_to_download_path)]
        files_path = [x for x in files_path if os.path.isfile(x)]
        files_path = [x for x in files_path if x.endswith(('xls', 'xlsx', 'xlsm'))]
        files_path = [
                {
                    "path": path,
                    "name": os.path.basename(path),
                    "data": datetime.fromtimestamp(os.path.getmtime(path)).strftime("%d/%m/%Y %H:%M:%S")
                }
                for path in files_path
            ]
        
        return JsonResponse(files_path, safe=False)
            
    return JsonResponse(['Nenhum arquivo para download'], safe=False)


@login_required()
@permission_required('tasks.consolidarDadosMultiplasPlanilhas', raise_exception=True)
def download_file(request: WSGIRequest):
    if request.method == "GET":
        file_path = request.GET.get('path')
        if file_path:
            if os.path.exists(file_path):
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(fh.read(), content_type="application/octet-stream")
                    response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                    return response
            raise Http404
    return redirect('index_consolidarDadosMultiplasPlanilhas')

