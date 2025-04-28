from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth.decorators import login_required, permission_required
from Central_RPA.utils import Utils, os
from datetime import datetime
from . import models
from typing import Literal
import json
from tasks.views import TarefasValidas
import shutil

tarefas = TarefasValidas()

@login_required
def test(request:WSGIRequest):
    
    return JsonResponse({'status': 'ok', 'message': 'Test endpoint is working!'})

########### Relatorio Abertura Despesas ###########

class Config:
    @property
    def nome_tarefa(self):
        self.__atualizar()
        return self.__nome_tarefa
    
    @property
    def caminho_tarefa(self):   
        self.__atualizar()
        return self.__caminho_tarefa
    
    def __init__(self):
        pass
    
    def __atualizar(self):
        try:
            self.__nome_tarefa = models.FinanceiroConfig.objects.get(nome='nome_tarefa').valor
        except:
            models.FinanceiroConfig.objects.create(nome='nome_tarefa', valor='')
            self.__nome_tarefa = models.FinanceiroConfig.objects.get(nome='nome_tarefa').valor
            
        try:
            self.__caminho_tarefa = models.FinanceiroConfig.objects.get(nome='caminho_tarefa').valor
        except:
            models.FinanceiroConfig.objects.create(nome='caminho_tarefa', valor='')
            self.__caminho_tarefa = models.FinanceiroConfig.objects.get(nome='caminho_tarefa').valor
            
    def set_value(self, tag:Literal['nome_tarefa', 'caminho_tarefa'], value:str):
        models.FinanceiroConfig.objects.filter(nome=tag).update(valor=value)

config_relatAberturaDesp = Config()
print(config_relatAberturaDesp.nome_tarefa, config_relatAberturaDesp.caminho_tarefa)

@login_required
@Utils.superUser_required
def adminConfig_relatAberturaDesp(request: WSGIRequest):
    if request.method == "POST":
        mensagem = "Retorno do envio:\n\n"
        
        value = request.POST.get('nome_tarefa')
        if value:
            config_relatAberturaDesp.set_value(tag='nome_tarefa', value=value)
            mensagem += f"Nome da tarefa atualizado para '{value}'\n\n"
        else:
            mensagem += f"Nome da tarefa não foi atualizado\n\n"
        
        value = request.POST.get('caminho_tarefa')
        if (value) and os.path.exists(value):
            config_relatAberturaDesp.set_value(tag='caminho_tarefa', value=value)
            mensagem += f"Caminho da tarefa atualizado para '{value}'\n\n"
        else:
            mensagem += f"Caminho da tarefa não foi atualizado\n\n"

        mensagem += f"Finalizado!\n\n"
        
        return Utils.message_retorno(request, text=mensagem, name_route='index_relatAberturaDesp')
    
    return redirect('index_relatAberturaDesp')

@login_required
@permission_required('tasks.financeiro_relatAberturaDesp', raise_exception=True)
def index_relatAberturaDesp(request:WSGIRequest):
    print(tarefas.listar_tarefas())
    content = {
        "teste": "testado",
        "nome_tarefa": config_relatAberturaDesp.nome_tarefa,
        "caminho_tarefa": config_relatAberturaDesp.caminho_tarefa,
        "date": datetime.now().strftime("%Y-%m-%d"),
    }
    
    return render(request, 'relatAberturaDesp/index.html', content)


@login_required
@permission_required('tasks.financeiro_relatAberturaDesp', raise_exception=True)
def upFiles_relatAberturaDesp(request:WSGIRequest):
    if request.method == "POST":
        lista_files = ['desp_adm', 'desp_comercial','outras_despesas']
        mensagem = "Retorno do envio:\n\n"
        
        date:datetime = datetime.strptime(request.POST.get('date'), "%Y-%m-%d")
        
        files_to_execute = {"files_path": {}, "date": date.isoformat()}
        
        path_file = os.path.join(config_relatAberturaDesp.caminho_tarefa, 'files')
        for file in os.listdir(path_file):
            file = os.path.join(path_file, file)
            os.unlink(file)
            
        for file_key in lista_files:
            file = request.FILES.get(file_key)
            if file:
                if file.name.lower().endswith(('.xlsx', '.xls', 'xlsm')):
                    path_file_final = Utils.upfile(path=path_file, file=file)
                    files_to_execute["files_path"][file_key] = path_file_final
                    mensagem += f"Arquivo '{file.name}' enviado com sucesso\n\n"
                else:
                    mensagem += f"Arquivo '{file.name}' não é um arquivo Excel\n\n"
                    continue
        
        date = request.POST.get('date')
               
        if files_to_execute["files_path"]:
            path_json = os.path.join(config_relatAberturaDesp.caminho_tarefa, 'json')
            path_json = os.path.join(path_json, 'args.json')
            with open(path_json, 'w', encoding='utf-8') as _file:
                json.dump(files_to_execute, _file)
            
            ##### start task #####
            for tarefa in tarefas.listar_tarefas():
                if tarefa.nome == config_relatAberturaDesp.nome_tarefa:
                    tarefa.executar()
            ######################          
            
            mensagem += f"Arquivos a serem executados '{len(files_to_execute['files_path'])}'\n\n"
        else:
            mensagem += "Nenhum arquivo valido para execução\n\n"
        
        return Utils.message_retorno(request, text=mensagem, name_route='index_relatAberturaDesp')
            
    return redirect('index_relatAberturaDesp')

@login_required
@permission_required('tasks.financeiro_relatAberturaDesp', raise_exception=True)
def tarefa_status(request: WSGIRequest):
    if request.method == "GET":
        for tarefa in tarefas.listar_tarefas():
            if tarefa.nome == config_relatAberturaDesp.nome_tarefa:
                return JsonResponse({'status': tarefa.status()})
    
    return JsonResponse({'status': None})

@login_required
@permission_required('tasks.financeiro_relatAberturaDesp', raise_exception=True)
def lista_files(request: WSGIRequest):
    if request.method == "GET":
        _lista_files = []
        path_file = os.path.join(config_relatAberturaDesp.caminho_tarefa, 'files')
        if os.path.exists(path_file):
            for file in os.listdir(path_file):
                file = os.path.join(path_file, file)
                if os.path.isfile(file):
                    mod_datetime = datetime.fromtimestamp(os.path.getmtime(file))
                    _lista_files.append({
                        "name": os.path.basename(file),
                        "caminho": file,
                        "tamanho": f"{round(os.path.getsize(file) / 1024, 2)} KB",
                        "data": mod_datetime.strftime("%Y-%m-%d %H:%M:%S")
                    })
        
        return JsonResponse(_lista_files, safe=False)
    
    return JsonResponse({'status': None})

##################################################