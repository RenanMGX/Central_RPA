from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth.decorators import login_required, permission_required
import os
from .models import InsumoObraPath
from Central_RPA.utils import Utils

class TargetPath:
    sub_path = os.path.normpath('insumosObras/arquivos')
    @staticmethod   
    def path():
        try:
            base_path = InsumoObraPath.objects.get(pk=1).path
        except InsumoObraPath.DoesNotExist:
            base_path = os.getcwd()
        if not base_path:
            base_path = os.getcwd()
        return os.path.normpath(os.path.join(base_path, TargetPath.sub_path))

        
#raiz_path = os.path.join(os.getcwd(), 'insumosObras/arquivos')

def listar_arquivos(path):
    path = os.path.join(TargetPath.path() ,path)
    if not os.path.exists(path):
        os.makedirs(path)
    result = {}
    for file in os.listdir(path):
        result[file] = os.path.normpath(os.path.join(path, file))
    return result

@login_required
@permission_required('tasks.insumosObras', raise_exception=True)
def index(request:WSGIRequest):
    content = {
        'patrimarFiles' : listar_arquivos('patrimar'),
        'novolarFiles': listar_arquivos('novolar'),
        'targetPath': TargetPath.path().replace(TargetPath.sub_path, '')
    }
    return render(request, 'insumosObras_index.html', content)

@login_required
@permission_required('tasks.insumosObras', raise_exception=True)
def delete(request:WSGIRequest):
    if request.method == 'POST':
        if (patrimar_files:=request.POST.get('del_patrimar')):
            patrimar_files = patrimar_files.split(',')
            for file in patrimar_files:
                if os.path.isfile(file):
                    os.remove(file)
                    
        if (patrimar_files:=request.POST.get('del_novolar')):
            patrimar_files = patrimar_files.split(',')
            for file in patrimar_files:
                if os.path.isfile(file):
                    os.remove(file)
                    
    return redirect('insumosObras_index')

@login_required
@permission_required('tasks.insumosObras', raise_exception=True)
def create(request:WSGIRequest, folder):
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        upload_path = os.path.join(TargetPath.path(), folder)
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)
        for file in files:
            with open(os.path.join(upload_path, file.name), 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
    
    return redirect('insumosObras_index')

@login_required
@Utils.superUser_required
def set_path(request:WSGIRequest):
    if request.method == 'POST':
        if(path:=request.POST.get('path')):
            if not path:
                path = os.getcwd()
            if os.path.exists(path):
                print("alterou para", path)
                InsumoObraPath.objects.update_or_create(pk=1, defaults={'path':path})
    return redirect('insumosObras_index')