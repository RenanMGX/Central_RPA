from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest #for Typing
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse, HttpResponse, Http404
from datetime import datetime
from tasks.views import tarefas_validas
from time import sleep
from .Entities.preparar import Preparar
import os

@login_required()
@permission_required('tasks.processComi', raise_exception=True)
def index(request: WSGIRequest):
    content = {
        "date": datetime.now().strftime("%Y-%m-%d")
    }
    return render(request, 'processComi.html', content)


@login_required()
@permission_required('tasks.processComi', raise_exception=True)
def start(request: WSGIRequest):
    if request.method == "POST":
        date = ""
        if (x:=request.POST.get('data')):
            date = datetime.strptime(x, "%Y-%m-%d")
            
        if date:
            tarefas_validas.listar_tarefas()
            for task in tarefas_validas.tarefas:
                if task.nome == r"Automações\ProcessoComissao":
                    #print(task.status())
                    Preparar.limpar_pasta()
                    if Preparar.send_param(date):
                        task.executar()
                    # sleep(1)
                    # while not task.status() == "Pronto":
                    #     print("esperando")
                    #     sleep(1)
        
    return redirect('processComi_index')


@login_required()
@permission_required('tasks.processComi', raise_exception=True)
def status(request: WSGIRequest):
    result = {}
    tarefas_validas.listar_tarefas()
    for task in tarefas_validas.tarefas:
        if task.nome == r"Automações\ProcessoComissao":
            result = {
                "status": task.status()
            }
    return JsonResponse(result)

@login_required()
@permission_required('tasks.processComi', raise_exception=True)
def list_files(request: WSGIRequest):
    result = {}
    for file in Preparar.verificar_pasta():
        result[os.path.basename(file)] = file

    return JsonResponse(result)

@login_required()
@permission_required('tasks.processComi', raise_exception=True)
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
    return redirect('processComi_index')