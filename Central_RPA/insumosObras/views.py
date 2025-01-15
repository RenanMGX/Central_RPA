from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth.decorators import login_required, permission_required
import os

raiz_path = os.path.join(os.getcwd(), 'insumosObras/arquivos')

def listar_arquivos(path):
    path = os.path.join(raiz_path ,path)
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
        'novolarFiles': listar_arquivos('novolar')
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
        upload_path = os.path.join(raiz_path, folder)
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)
        for file in files:
            with open(os.path.join(upload_path, file.name), 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
    
    return redirect('insumosObras_index')
