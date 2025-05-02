from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.handlers.wsgi import WSGIRequest
from .Entities.registros import Registros
from django.contrib.auth.decorators import login_required, permission_required
from Central_RPA.utils import Utils
from Financeiro import models
from typing import Literal
import os
import subprocess

def teste(request:WSGIRequest):
    return JsonResponse({"status": "teste"})

class Config:   
    @property
    def caminho_imobmeExtract(self):   
        self.__atualizar()
        return self.__caminho_imobmeExtract
    
    def __init__(self):
        pass
    
    def __atualizar(self):
            
        try:
            self.__caminho_imobmeExtract = models.FinanceiroConfig.objects.get(nome='caminho_imobmeExtract').valor
        except:
            models.FinanceiroConfig.objects.create(nome='caminho_imobmeExtract', valor='')
            self.__caminho_imobmeExtract = models.FinanceiroConfig.objects.get(nome='caminho_imobmeExtract').valor
            
    def set_value(self, tag:Literal['caminho_imobmeExtract'], value:str):
        models.FinanceiroConfig.objects.filter(nome=tag).update(valor=value)

config_params= Config()

######### Config Integração Web ###########
    
    
@login_required
@Utils.superUser_required
def adminConfig_ConfigIntegraWeb(request: WSGIRequest):
    if request.method == "POST":
        mensagem = "Retorno do envio:\n\n"
        
        value = request.POST.get('caminho_imobmeExtract')
        if value:
            if os.path.exists(value):
                config_params.set_value(tag='caminho_imobmeExtract', value=value)
                mensagem += f"Nome da tarefa atualizado para '{value}'\n\n"
            else:
                mensagem += f"Nome da tarefa não foi atualizado, caminho não existe\n\n"
        else:
            mensagem += f"Nome da tarefa não foi atualizado\n\n"

        mensagem += f"Finalizado!\n\n"
        
        return Utils.message_retorno(request, text=mensagem, name_route='index_ConfigIntegraWeb')
    
    return redirect('index_ConfigIntegraWeb')



CONFIG_VCRED_PERMISSIONS = "tasks.creditoImobiliario_configVCRED"

@login_required()
@permission_required(CONFIG_VCRED_PERMISSIONS, raise_exception=True)
def index_ConfigIntegraWeb(request:WSGIRequest):
    try:
        Registros(os.path.join(config_params.caminho_imobmeExtract, 'json', 'integraWeb_filtros_empreendimentos.json'))#type: ignore
        Registros(os.path.join(config_params.caminho_imobmeExtract, 'json',  'integraWeb_filtros_dadoscontrato.json'))#type: ignore
        valid = True
    except Exception as e:
        valid = False
        
    
    content = {
        "config_params": config_params.caminho_imobmeExtract,
        "valid": valid,
    }
    return render(request, 'configIntegraWeb/index.html', content)

@login_required()
@permission_required(CONFIG_VCRED_PERMISSIONS, raise_exception=True)
def filtros_ConfigIntegraWeb(request: WSGIRequest):
    filtros_empreendimentos = Registros(os.path.join(config_params.caminho_imobmeExtract, 'json',  'integraWeb_filtros_empreendimentos.json'))#type: ignore
    filtros_dadoscontrato = Registros(os.path.join(config_params.caminho_imobmeExtract, 'json',  'integraWeb_filtros_dadoscontrato.json'))#type: ignore
    if request.method == 'GET':
        tag = request.GET.get('tag')
        if tag == "filtros_empreendimentos":
            return JsonResponse(filtros_empreendimentos.load_all(), safe=True)
        elif tag == "filtros_dadoscontrato":
            return JsonResponse(filtros_dadoscontrato.load_all(), safe=True)
    
    
    return JsonResponse({}, safe=True)

@login_required()
@permission_required(CONFIG_VCRED_PERMISSIONS, raise_exception=True)
def add_filtro_ConfigIntegraWeb(request: WSGIRequest):
    filtros_empreendimentos = Registros(os.path.join(config_params.caminho_imobmeExtract, 'json',  'integraWeb_filtros_empreendimentos.json'))#type: ignore
    filtros_dadoscontrato = Registros(os.path.join(config_params.caminho_imobmeExtract, 'json',  'integraWeb_filtros_dadoscontrato.json'))#type: ignore
    if request.method == 'POST':

        tag = request.POST.get('tag')
        _type = request.POST.get('type')
        
        if _type == "columnsToRemove":
            columns = request.POST.getlist('columns')[0].split(",")
            columns = [col.strip() for col in columns if col.strip() != ""]
            if tag == "filtros_empreendimentos":
                filtros_empreendimentos.register_columnsToRemove(columns=columns)
            elif tag == "filtros_dadoscontrato":
                filtros_dadoscontrato.register_columnsToRemove(columns=columns)
        
        elif _type == "columnsToKeep":
            columns = request.POST.getlist('columns')[0].split(",")
            columns = [col.strip() for col in columns if col.strip() != ""]
            if tag == "filtros_empreendimentos":
                filtros_empreendimentos.register_columnsToKeep(columns=columns)
            elif tag == "filtros_dadoscontrato":
                filtros_dadoscontrato.register_columnsToKeep(columns=columns)
       
        elif _type == "rowsToKeep":
            column = request.POST['column']
            value_in_rows = request.POST.getlist('value_in_rows')[0].split(",")
            value_in_rows = [col.strip() for col in value_in_rows if col.strip() != ""]
            if tag == "filtros_empreendimentos":
                filtros_empreendimentos.register_rowsToKeep(column=column, value_in_rows=value_in_rows)
            elif tag == "filtros_dadoscontrato":
                filtros_dadoscontrato.register_rowsToKeep(column=column, value_in_rows=value_in_rows)
        
        elif _type == "rowsToRemove":
            column = request.POST['column']
            value_in_rows = request.POST.getlist('value_in_rows')[0].split(",")
            value_in_rows = [col.strip() for col in value_in_rows if col.strip() != ""]
            if tag == "filtros_empreendimentos":
                filtros_empreendimentos.register_rowsToRemove(column=column, value_in_rows=value_in_rows)
            elif tag == "filtros_dadoscontrato":
                filtros_dadoscontrato.register_rowsToRemove(column=column, value_in_rows=value_in_rows)
                
        return Utils.message_retorno(request, f"Filtro {tag} foi Criado!", name_route="index_ConfigIntegraWeb")
    return redirect('index_ConfigIntegraWeb')

@login_required()
@permission_required(CONFIG_VCRED_PERMISSIONS, raise_exception=True)
def delete_alterar_filtro_ConfigIntegraWeb(request: WSGIRequest):
    filtros_empreendimentos = Registros(os.path.join(config_params.caminho_imobmeExtract, 'json',  'integraWeb_filtros_empreendimentos.json'))#type: ignore
    filtros_dadoscontrato = Registros(os.path.join(config_params.caminho_imobmeExtract, 'json',  'integraWeb_filtros_dadoscontrato.json'))#type: ignore
    if request.method == 'GET':
        tag = request.GET.get('tag')

        if tag == "filtros_empreendimentos":
            filtros_empreendimentos.delete(request.GET['index'])
        elif tag == "filtros_dadoscontrato":
            filtros_dadoscontrato.delete(request.GET['index'])
            
        return Utils.message_retorno(request, f"Filtro {tag} foi apagado!", name_route="index_ConfigIntegraWeb")
    elif request.method == "POST":
        
        tag = request.POST.get('tag')

        if tag == "filtros_empreendimentos":
            filtros_empreendimentos.delete(request.POST['index'])
        elif tag == "filtros_dadoscontrato":
            filtros_dadoscontrato.delete(request.POST['index'])
        
        
        add_filtro_ConfigIntegraWeb(request)

        return Utils.message_retorno(request, f"Filtro {tag} foi alterado!", name_route="index_ConfigIntegraWeb")
    return redirect('index_ConfigIntegraWeb')


@login_required()
@permission_required(CONFIG_VCRED_PERMISSIONS, raise_exception=True)
def testar_filtro_ConfigIntegraWeb(request: WSGIRequest):
    path = str(config_params.caminho_imobmeExtract)
    file_py = os.path.join(path, 'IntegraçãoWEB_DJANGO.py')
    executable_path = os.path.join(path, 'venv', 'Scripts', 'python.exe')
    
    tag = request.GET.get('tag')
    if (os.path.exists(executable_path)) and (os.path.exists(file_py)):
        subprocess.run([executable_path, file_py], cwd=path)

        path = os.path.join(path, 'temp_IntegracaoWeb_Django')
        for file in os.listdir(path):
            file = os.path.join(path, file)
            if os.path.isfile(file):
                if file.lower().endswith('.csv'):
                    if tag == "filtros_empreendimentos":
                        if "empreendimentos" in file.lower():
                            return Utils.download_file(file)
                    elif tag == "filtros_dadoscontrato":
                        if "dadoscontrato" in file.lower():
                            return Utils.download_file(file)                 
                    
    
    #return JsonResponse({"status": "teste"})
    return redirect('index_ConfigIntegraWeb')
