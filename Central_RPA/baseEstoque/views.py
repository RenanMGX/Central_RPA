from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.core.handlers.wsgi import WSGIRequest
from tasks.models import Tarefas
import json
import os
from getpass import getuser
from django.http import HttpResponse, Http404
from django.urls import reverse
from datetime import datetime
import shutil
import pandas as pd
from tasks.views import tarefas_validas

def start_task(pk) -> bool:
    pk = int(pk)
    tarefas_validas.listar_tarefas()
    for tarefa in tarefas_validas.tarefas:
        if tarefa.pk == pk:
            tarefa.executar()
            return True
    return False

@login_required()
@permission_required('tasks.baseEstoque', raise_exception=True) #type: ignore   
def index(requests:WSGIRequest):
    task = Tarefas.objects.filter(tarefa__contains=r"VGV_Empreendimentos")
    content = {
        'item': task[0] if task else None
    }
    return render(requests, "baseEstoque.html", content)


@login_required()
@permission_required('tasks.baseEstoque', raise_exception=True) #type: ignore   
def file(requests:WSGIRequest):
    task = Tarefas.objects.filter(tarefa__contains=r"VGV_Empreendimentos")
    if task:
        task = task[0]
        infor:dict = json.loads(str(task.infor))
        
        path_download = f'C:\\Users\\{getuser()}\\Downloads'
        if not os.path.exists(path_download):
            return message_retorno(f'Erro 02: a pasta do download não encontrada "{path_download}"')
        
        path_rpa:str = infor['vgv'] if infor.get('vgv') else ""

        if os.path.exists(path_rpa):
            if requests.FILES.get('file'):
                file = requests.FILES['file']

                if (file.name.endswith('xlsx')) or (file.name.endswith('xlsm')) or (file.name.endswith('xls')):
                    temp_name = os.path.join(path_download, datetime.now().strftime(f"%Y%m%d%H%M%S_{file.name}"))
                    with open(temp_name, 'wb+') as _file:
                        for chunk in file.chunks():
                            _file.write(chunk) 
                    
                    if not infor.get('sheet'):
                        return message_retorno("Erro 06: sheet não encontrada")
                        
                    sheet = infor.get('sheet')
                     
                    try:
                        pd.read_excel(temp_name, sheet_name=infor.get('sheet'))
                    except:
                        return message_retorno(f"Erro 05: planilha inválida sheet '{sheet}' não encontrada")
                        
                    if requests.POST.get('vgv_empreendimento'):
                        if not os.path.exists(os.path.join(path_rpa, 'IC_BASE')):
                            os.makedirs(os.path.join(path_rpa, 'IC_BASE'))
                        final_path = os.path.join(path_rpa, 'IC_BASE', 'Base Estoque.xlsx')
                        shutil.copy(temp_name, final_path)
                        start_task(task.pk)
                    
                    
                    #if requests.POST.get('integração_web'):
                        #print("executou integração_web")
                    
                    os.remove(temp_name)
                    
                    return message_retorno("Concluido: Arquivo Copiado!")
                else:
                    return message_retorno("Erro 04: é aceito apenas arquivos Excel") 
            else:
                return message_retorno("Erro 03: Arquivo ausente")
        else:
            return message_retorno(f'Erro 02: pasta do RPA não encontrada "{path_rpa}"')
    else:
        return message_retorno("Erro 01: Tarefa não encontrada")

def message_retorno(text, name_route="baseEstoque_index"):
    try:
        route = reverse(name_route)
        msg = f"""
        <script>
        alert('{text.replace("'", "").replace('"', "").replace("\\", "")}');
        window.location.href='{route}';
        </script> 
        """
        return HttpResponse(msg)
    except:
        raise Http404(f"rota '{name_route}' não encontrada")
