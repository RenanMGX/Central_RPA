
import subprocess
import re

class Tarefas:
    @property
    def nome(self) -> str:
        return self.__nome_tarefa
    
    def __init__(self, nome_tarefa:str) -> None:
        self.__nome_tarefa:str = nome_tarefa
        
    def __str__(self) -> str:
        return self.nome
    
    # Função para verificar o status de uma tarefa
    def status(self) -> str:
        result = subprocess.run(['schtasks', '/query', '/tn', self.__nome_tarefa, '/fo', 'LIST', '/v'], capture_output=True, text=True, encoding='cp850')
        result = re.search(r'Status:.*?\n', result.stdout)
        if result:
            result = re.search(r'(?<=Status: )[\d\D]+', result.group())
            if result:
                result = result.group().replace("\n",'')
                return re.sub(r'[ ]{2,}' ,'', result)
                
        return "None"
    
    @staticmethod
    def executar(nome_tarefa):
        result = subprocess.run(['schtasks', '/run', '/tn', nome_tarefa], capture_output=True, text=True)
        return result.stdout





# Função para listar todas as tarefas
def listar_tarefas():
    result = subprocess.run(['schtasks', '/query'], capture_output=True, text=True)
    return result.stdout

# Função para executar uma tarefa específica
def executar_tarefa(nome_tarefa):
    result = subprocess.run(['schtasks', '/run', '/tn', nome_tarefa], capture_output=True, text=True)
    return result.stdout

