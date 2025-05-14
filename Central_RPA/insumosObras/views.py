from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse, HttpResponse, Http404
import os
from .models import InsumoObraPath
from Central_RPA.utils import Utils
from typing import List
import openpyxl
from tasks.Entities.new_tasks import NewTasks
from datetime import datetime

#task = NewTasks(value=r"Nome da tarefa: Automações\Qualidade\InsumosObra", pasta=r".Automações\Qualidade")

    
def up_date() -> NewTasks:
    try:
        nome_tarefa = InsumoObraPath.objects.get(pk=2).path
    except:
        nome_tarefa = ""
        
    try:
        past =  InsumoObraPath.objects.get(pk=3).path
    except InsumoObraPath.DoesNotExist:
            ast = ""
        
    try:
        return NewTasks(value=nome_tarefa, pasta=past)
    except:
        return None #type:ignore

 
task = up_date() #type:ignore
  

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
    
    @staticmethod
    def nome_da_tarefa():
        param = ""
        try:
            param = InsumoObraPath.objects.get(pk=2).path
        except InsumoObraPath.DoesNotExist:
            param = ""
        return param
    
    @staticmethod
    def pasta():
        param = ""
        try:
            param = InsumoObraPath.objects.get(pk=3).path
        except InsumoObraPath.DoesNotExist:
            param = ""
        return param



def listar_arquivos(path):
    path = os.path.join(TargetPath.path() ,path)
    if not os.path.exists(path):
        os.makedirs(path)
    result = {}
    for file in os.listdir(path):
        result[file] = os.path.normpath(os.path.join(path, file))
    return result


def listar_arquivo_completo(path):
    path = os.path.join(TargetPath.path() ,path)
    if not os.path.exists(path):
        os.makedirs(path)
    
    result = {}
    for file in os.listdir(path):
        file = os.path.normpath(os.path.join(path, file))
        result["name"] = os.path.basename(file)
        result["data"] = datetime.fromtimestamp(os.path.getmtime(file)).strftime('%d/%m/%Y %H:%M:%S')
        result["tamanho"] = str(round(os.path.getsize(file) / 1024, 2)) + " KB"
        result["path"] = file
        
    return result



@login_required
@permission_required('tasks.insumosObras', raise_exception=True)
def index(request:WSGIRequest):
    print(listar_arquivos('patrimar'))
    content = {
        'patrimarFiles' : listar_arquivos('patrimar'),
        'novolarFiles': listar_arquivos('novolar'),
        'convert': listar_arquivo_completo('convert'),
        'finalPath': listar_arquivo_completo('final'),
        'targetPath': TargetPath.path().replace(TargetPath.sub_path, ''),
        'nome_da_tarefa': TargetPath.nome_da_tarefa(),
        'pasta': TargetPath.pasta()
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
        
        mod = request.POST.get('mod')
        
        valid_sheet = "Base de Dados" if mod == "add" else "CONVERSÃO MATERIAIS APLIC." if mod == "convert" else "None"
        valids_columns =["TxtBreveMaterial", "Cen.", "Quantidade", "Dt.lçto."] if mod == "add" else ["TxtBreveMaterial", "UM", "PARÂMETRO", "FINALIDADE 1" , "FATOR DE CONVERSÃO"] if mod == "convert" else ["None"]

        if mod == "convert":
            for temp_file in os.listdir(upload_path):
                os.unlink(os.path.join(upload_path, temp_file))
        
        errors = []
        for file in files:
            if file.name.lower().endswith(('xls', 'xlsx', 'xlsm')):
                file_path = os.path.join(upload_path, file.name)
                with open(file_path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                try:
                    wb = openpyxl.load_workbook(file_path)
                    if not valid_sheet in wb.sheetnames:
                        errors.append(f"a planilha {file.name} não possui a aba 'Base de Dados'")
                        wb.close()
                        os.unlink(file_path)
                        continue
                    else:
                        columns = [cell.value for cell in wb[valid_sheet][1]]
                        if not all(item in columns for item in valids_columns):
                            errors.append(f"a planilha {file.name} não possui todas as colunas necessárias {valids_columns}")
                            wb.close()
                            os.unlink(file_path)
                            continue
                    wb.close()
                except Exception as err:
                    errors.append(f"Erro ao abrir a planilha {file.name}: {err}")
                    os.unlink(file_path)
            else:
                errors.append(f"a planilha {file.name} não é um arquivo excel")
        
        #print("aqui")
        if errors:
            return Utils.message_retorno(request, text=f"Erro ao enviar arquivos\n{'\n'.join(errors)}", name_route='insumosObras_index')
        else:
            return Utils.message_retorno(request, text=f"Envio Concluido sem nenhum error!", name_route='insumosObras_index')
        
    return redirect('insumosObras_index')
    

@login_required
@Utils.superUser_required
def set_path(request:WSGIRequest):
    if request.method == 'POST':
        if(path:=request.POST.get('path')):
            if not path:
                path = os.getcwd()
            if os.path.exists(path):
                #print("alterou para", path)
                InsumoObraPath.objects.update_or_create(pk=1, defaults={'path':path})
                return Utils.message_retorno(request, text="Alteração Concluida", name_route='insumosObras_index')
    return redirect('insumosObras_index')

@login_required
@Utils.superUser_required
def set_nome_da_tarefa(request:WSGIRequest):
    if request.method == 'POST':
        if(param:=request.POST.get('nome_da_tarefa')):
            if not param:
                param = ""
            InsumoObraPath.objects.update_or_create(pk=2, defaults={'path':param})
            return Utils.message_retorno(request, text="Alteração Concluida", name_route='insumosObras_index')
    return redirect('insumosObras_index')

@login_required
@Utils.superUser_required
def set_pasta(request:WSGIRequest):
    if request.method == 'POST':
        if(param:=request.POST.get('pasta')):
            if not param:
                param = ""
            InsumoObraPath.objects.update_or_create(pk=3, defaults={'path':param})
            return Utils.message_retorno(request, text="Alteração Concluida", name_route='insumosObras_index')
    return redirect('insumosObras_index')

@login_required
@permission_required('tasks.insumosObras', raise_exception=True)
def status(request:WSGIRequest):
    return JsonResponse({'status': task.status})


@login_required
@permission_required('tasks.insumosObras', raise_exception=True)
def start(request:WSGIRequest):
    #print(request.method)
    if request.method == 'GET':
        task.start()

    return JsonResponse({})

@login_required()
@permission_required('tasks.insumosObras', raise_exception=True)
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
    return redirect('insumosObras_index')
