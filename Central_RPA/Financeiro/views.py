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
from dateutil.relativedelta import relativedelta
import json

tarefas = TarefasValidas()

@login_required
def test(request:WSGIRequest):
    
    return JsonResponse({'status': 'ok', 'message': 'Test endpoint is working!'})

########### Relatorio Abertura Despesas ###########

class Config_relatAberturaDesp:
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

config_relatAberturaDesp = Config_relatAberturaDesp()

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
    #print(tarefas.listar_tarefas())
    content = {
        "teste": "testado",
        "nome_tarefa": config_relatAberturaDesp.nome_tarefa,
        "caminho_tarefa": config_relatAberturaDesp.caminho_tarefa,
        "date": (datetime.now().replace(day=1) - relativedelta(months=1)).strftime("%Y-%m-%d"),
    }
    
    return render(request, 'relatAberturaDesp/index.html', content)


@login_required
@permission_required('tasks.financeiro_relatAberturaDesp', raise_exception=True)
def upFiles_relatAberturaDesp(request:WSGIRequest):
    if request.method == "POST":
        lista_files = ['desp_adm', 'desp_comercial','outras_despesas']
        mensagem = "Retorno do envio:\n\n"
        
        
        date:datetime = datetime.strptime(request.POST.get('date'), "%Y-%m-%d") #type: ignore
        
        files_to_execute = {"files_path": {}, "date": date.isoformat()}
        
        path_file = os.path.join(config_relatAberturaDesp.caminho_tarefa, 'files')#type: ignore
        for file in os.listdir(path_file):
            file = os.path.join(path_file, file)
            os.unlink(file)
            
        for file_key in lista_files:
            file = request.FILES.get(file_key)
            if file:
                if file.name.lower().endswith(('.xlsx', '.xls', 'xlsm')):
                    path_file_final = Utils.upfile(path=path_file, file=file)#type: ignore
                    files_to_execute["files_path"][file_key] = path_file_final
                    mensagem += f"Arquivo '{file.name}' enviado com sucesso\n\n"
                else:
                    mensagem += f"Arquivo '{file.name}' não é um arquivo Excel\n\n"
                    continue
        
        date = request.POST.get('date')#type: ignore
               
        if files_to_execute["files_path"]:
            path_json = os.path.join(config_relatAberturaDesp.caminho_tarefa, 'json')#type: ignore
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
def tarefa_status_relatAberturaDesp(request: WSGIRequest):
    if request.method == "GET":
        for tarefa in tarefas.listar_tarefas():
            if tarefa.nome == config_relatAberturaDesp.nome_tarefa:
                return JsonResponse({'status': tarefa.status()})
    
    return JsonResponse({'status': None})

@login_required
@permission_required('tasks.financeiro_relatAberturaDesp', raise_exception=True)
def lista_files_relatAberturaDesp(request: WSGIRequest):
    if request.method == "GET":
        _lista_files = []
        path_file = os.path.join(config_relatAberturaDesp.caminho_tarefa, 'files')#type: ignore
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

@login_required
@permission_required('tasks.financeiro_relatAberturaDesp', raise_exception=True)
def log_relatAberturaDesp(request: WSGIRequest):
    if request.method == "GET":
        path_log = os.path.join(config_relatAberturaDesp.caminho_tarefa, 'json', 'informativo.json')#type: ignore
        if os.path.exists(path_log):
            with open(path_log, 'r', encoding='utf-8') as _file:
                lista:list = json.load(_file)
                lista.reverse()
                return JsonResponse(lista, safe=False)
        #print(path_log)
        
        
    return JsonResponse([], safe=False)

###################################################

########### Relatorio Abertura Despesas ###########

class Config_cadastroVtax:
    @property
    def nome_tarefa_cadastroVtax(self):
        self.__atualizar()
        return self.__nome_tarefa_cadastroVtax
    
    @property
    def caminho_tarefa_cadastroVtax(self):   
        self.__atualizar()
        return self.__caminho_tarefa_cadastroVtax
    
    def __init__(self):
        pass
    
    def __atualizar(self):
        try:
            self.__nome_tarefa_cadastroVtax = models.FinanceiroConfig.objects.get(nome='nome_tarefa_cadastroVtax').valor
        except:
            models.FinanceiroConfig.objects.create(nome='nome_tarefa_cadastroVtax', valor='')
            self.__nome_tarefa_cadastroVtax = models.FinanceiroConfig.objects.get(nome='nome_tarefa_cadastroVtax').valor
            
        try:
            self.__caminho_tarefa_cadastroVtax = models.FinanceiroConfig.objects.get(nome='caminho_tarefa_cadastroVtax').valor
        except:
            models.FinanceiroConfig.objects.create(nome='caminho_tarefa_cadastroVtax', valor='')
            self.__caminho_tarefa_cadastroVtax = models.FinanceiroConfig.objects.get(nome='caminho_tarefa_cadastroVtax').valor
            
    def set_value(self, tag:Literal['nome_tarefa_cadastroVtax', 'caminho_tarefa_cadastroVtax'], value:str):
        models.FinanceiroConfig.objects.filter(nome=tag).update(valor=value)

config_cadastroVtax = Config_cadastroVtax()


    
@login_required
@Utils.superUser_required
def adminConfig_cadastroVtax(request: WSGIRequest):
    if request.method == "POST":
        mensagem = "Retorno do envio:\n\n"
        
        nome_tarefa = 'nome_tarefa_cadastroVtax'
        value = request.POST.get(nome_tarefa)
        if value:
            config_cadastroVtax.set_value(tag=nome_tarefa, value=value)
            mensagem += f"Nome da tarefa atualizado para '{value}'\n\n"
        else:
            mensagem += f"Nome da tarefa não foi atualizado\n\n"
        
        caminho_tarefa = 'caminho_tarefa_cadastroVtax'
        value = request.POST.get(caminho_tarefa)
        if (value) and os.path.exists(value):
            config_cadastroVtax.set_value(tag=caminho_tarefa, value=value)
            mensagem += f"Caminho da tarefa atualizado para '{value}'\n\n"
        else:
            mensagem += f"Caminho da tarefa não foi atualizado\n\n"

        mensagem += f"Finalizado!\n\n"
        
        return Utils.message_retorno(request, text=mensagem, name_route='index_cadastrarVtax')
    
    return redirect('index_cadastrarVtax')
    
    
@login_required
@permission_required('tasks.cadastrarVtax', raise_exception=True)
def index_cadastrarVtax(request: WSGIRequest):
    content = {
        "teste": "testado",
        "nome_tarefa_cadastroVtax": config_cadastroVtax.nome_tarefa_cadastroVtax,
        "caminho_tarefa_cadastroVtax": config_cadastroVtax.caminho_tarefa_cadastroVtax,
    }
    return render(request, 'cadastroVtax/index.html', content)

@login_required
@permission_required('tasks.cadastrarVtax', raise_exception=True)
def start_cadastrarVtax(request: WSGIRequest):
    if request.method == "POST":
        empresas = request.POST.get("empresas")
        print(request.POST)
        if empresas:
            empresas = empresas.split(",")
            cadastro_grupos_empresas_reinf = True if request.POST.get("cadastro_grupos_empresas_reinf") else False
            cadastro_representantes = True if request.POST.get("cadastro_representantes") else False
            cadastro_codigos_impostos = True if request.POST.get("cadastro_codigos_impostos") else False
            cadastro_codigo_servicos = True if request.POST.get("cadastro_codigo_servicos") else False
            
            param = {
                "empresas": empresas,
                "cadastro_grupos_empresas_reinf": cadastro_grupos_empresas_reinf,
                "cadastro_representantes": cadastro_representantes,
                "cadastro_codigos_impostos": cadastro_codigos_impostos,
                "cadastro_codigo_servicos": cadastro_codigo_servicos,
            } 
            
            if not (config_cadastroVtax.caminho_tarefa_cadastroVtax):
                return Utils.message_retorno(request, text="Caminho da tarefa não configurado", name_route='index_cadastrarVtax')
            
            path = os.path.join(config_cadastroVtax.caminho_tarefa_cadastroVtax, 'json', 'param.json')
            if not os.path.exists(os.path.dirname(path)):
                return Utils.message_retorno(request, text="Caminho da tarefa não encontrado", name_route='index_cadastrarVtax')
            with open(path, 'w') as _file:
                json.dump(param, _file, indent=4)
                
            for tarefa in tarefas.listar_tarefas():
                if tarefa.nome == config_cadastroVtax.nome_tarefa_cadastroVtax:
                    tarefa.executar()
        else:
            return Utils.message_retorno(request, text="Nenhuma empresa selecionada", name_route='index_cadastrarVtax')
    
    return redirect('index_cadastrarVtax')


@login_required
@permission_required('tasks.cadastrarVtax', raise_exception=True)
def retorno_cadastrarVtax(request: WSGIRequest):
    if request.method == "GET":
        #print(request.GET)
        if (mod:=request.GET.get("mod")):
            if mod == "status_automação":
                for tarefa in tarefas.listar_tarefas():
                    if tarefa.nome == config_cadastroVtax.nome_tarefa_cadastroVtax:
                        status = tarefa.status()
                        return JsonResponse({'status': status})
            
            elif mod == "logs":
                path = os.path.join(str(config_cadastroVtax.caminho_tarefa_cadastroVtax), 'json', 'informativo.json')
                if os.path.exists(path):
                    with open(path, 'r', encoding='utf-8') as _file:
                        logs = json.load(_file)
                        logs.reverse()
                        return JsonResponse(logs, safe=False)
        
        
        
    return JsonResponse({'status': 'ok', 'message': 'Test endpoint is working!'})
###################################################

############# Renegociação de Dividas #############

class Config_renegociarDividas:
    @property
    def nome_tarefa_renegociarDividas(self):
        self.__atualizar()
        return self.__nome_tarefa_renegociarDividas
    
    @property
    def caminho_tarefa_renegociarDividas(self):   
        self.__atualizar()
        return self.__caminho_tarefa_renegociarDividas
    
    def __init__(self):
        pass
    
    def __atualizar(self):
        try:
            self.__nome_tarefa_renegociarDividas = models.FinanceiroConfig.objects.get(nome='nome_tarefa_renegociarDividas').valor
        except:
            models.FinanceiroConfig.objects.create(nome='nome_tarefa_renegociarDividas', valor='')
            self.__nome_tarefa_renegociarDividas = models.FinanceiroConfig.objects.get(nome='nome_tarefa_renegociarDividas').valor
            
        try:
            self.__caminho_tarefa_renegociarDividas = models.FinanceiroConfig.objects.get(nome='caminho_tarefa_renegociarDividas').valor
        except:
            models.FinanceiroConfig.objects.create(nome='caminho_tarefa_renegociarDividas', valor='')
            self.__caminho_tarefa_renegociarDividas = models.FinanceiroConfig.objects.get(nome='caminho_tarefa_renegociarDividas').valor
            
    def set_value(self, tag:Literal['nome_tarefa_renegociarDividas', 'caminho_tarefa_renegociarDividas'], value:str):
        models.FinanceiroConfig.objects.filter(nome=tag).update(valor=value)

config_renegociarDividas = Config_renegociarDividas()


    
@login_required
@Utils.superUser_required
def adminConfig_renegociarDividas(request: WSGIRequest):
    if request.method == "POST":
        mensagem = "Retorno do envio:\n\n"
        
        nome_tarefa = 'nome_tarefa_renegociarDividas'
        value = request.POST.get(nome_tarefa)
        if value:
            config_renegociarDividas.set_value(tag=nome_tarefa, value=value)
            mensagem += f"Nome da tarefa atualizado para '{value}'\n\n"
        else:
            mensagem += f"Nome da tarefa não foi atualizado\n\n"
        
        caminho_tarefa = 'caminho_tarefa_renegociarDividas'
        value = request.POST.get(caminho_tarefa)
        if (value) and os.path.exists(value):
            config_renegociarDividas.set_value(tag=caminho_tarefa, value=value)
            mensagem += f"Caminho da tarefa atualizado para '{value}'\n\n"
        else:
            mensagem += f"Caminho da tarefa não foi atualizado\n\n"

        mensagem += f"Finalizado!\n\n"
        
        return Utils.message_retorno(request, text=mensagem, name_route='index_renegociarDividas')
    
    return redirect('index_renegociarDividas')



@login_required
@permission_required('tasks.renegociarDividas', raise_exception=True)
def index_renegociarDividas(request: WSGIRequest):
    content = {
        "teste": "testado",
        "nome_tarefa": config_renegociarDividas.nome_tarefa_renegociarDividas,
        "caminho_tarefa": config_renegociarDividas.caminho_tarefa_renegociarDividas,
    }
    return render(request, 'renegociarDividas/index.html', content)


@login_required
@permission_required('tasks.financeiro_renegociarDividas', raise_exception=True)
def upFiles_renegociarDividas(request:WSGIRequest):
    if request.method == "POST":
        lista_files = ['relatorio_kitei']
        mensagem = "Retorno do envio:\n\n"
        
        
        path_file = os.path.join(config_renegociarDividas.caminho_tarefa_renegociarDividas, 'file')#type: ignore
        for file in os.listdir(path_file):
            file = os.path.join(path_file, file)
            os.unlink(file)
            
        for file_key in lista_files:
            file = request.FILES.get(file_key)
            if file:
                if file.name.lower().endswith(('.xlsx', '.xls', 'xlsm')):
                    path_file_final = Utils.upfile(path=path_file, file=file)#type: ignore
                    if path_file_final:
                        ##### start task #####
                        for tarefa in tarefas.listar_tarefas():
                            if tarefa.nome == config_renegociarDividas.nome_tarefa_renegociarDividas:
                                tarefa.executar()
                    mensagem += f"Arquivo '{file.name}' enviado com sucesso\n\n"
                else:
                    mensagem += f"Arquivo '{file.name}' não é um arquivo Excel\n\n"
                    continue
        
        
        #return Utils.message_retorno(request, text=mensagem, name_route='index_renegociarDividas')
                       
        
        return Utils.message_retorno(request, text=mensagem, name_route='index_renegociarDividas')
            
    return redirect('index_renegociarDividas')


@login_required
@permission_required('tasks.renegociarDividas', raise_exception=True)
def status_renegociarDividas(request: WSGIRequest):
    if request.method == "GET":
        if (mod:=request.GET.get("mod")):
            if mod == "status_automação":
                for tarefa in tarefas.listar_tarefas():
                    if tarefa.nome == config_renegociarDividas.nome_tarefa_renegociarDividas:
                        tarefa_status = tarefa.status()
                        return JsonResponse({'status': tarefa_status})
       
    return JsonResponse({'status': 'ok', 'message': 'Test endpoint is working!'})

###################################################
