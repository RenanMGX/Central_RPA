from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth.decorators import login_required, permission_required
from . import models
from Central_RPA.utils import Utils
from django.http import JsonResponse
from .Entities.log_informativo import LogInformativo
import os


def test(request: WSGIRequest):
    return JsonResponse({"status": "ok"})

@login_required
@permission_required('tasks.consolidarDadosMultiplasPlanilhas', raise_exception=True)
def index(request: WSGIRequest):
    try:
        upload_path = models.Uploadpath.objects.get(pk=1).path
    except models.Uploadpath.DoesNotExist:
        upload_path = f'C:\\Users\\{os.getlogin()}\\Downloads'
        
    infomativo:list = LogInformativo(path=os.path.join(upload_path, 'informativoLog.json')).load()
    infomativo.reverse()

    content = {
        'upload_path': upload_path,
        'informativo': infomativo
    }
    return render(request, 'consolidarDadosMultiplasPlanilhas_index.html', content)

@login_required
@permission_required('tasks.consolidarDadosMultiplasPlanilhas', raise_exception=True)
def upload(request: WSGIRequest):
    try:
        upload_path = models.Uploadpath.objects.get(pk=1).path
    except models.Uploadpath.DoesNotExist:
        upload_path = f'C:\\Users\\{os.getlogin()}\\Downloads'
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
@permission_required('tasks.consolidarDadosMultiplasPlanilhas', raise_exception=True)
def log_informativo(request: WSGIRequest):
    try:
        upload_path = models.Uploadpath.objects.get(pk=1).path
    except models.Uploadpath.DoesNotExist:
        upload_path = f'C:\\Users\\{os.getlogin()}\\Downloads'
    
    infomativo:list = LogInformativo(path=os.path.join(upload_path, 'informativoLog.json')).load()
    infomativo.reverse()
    
    return JsonResponse(infomativo, safe=False)
    

