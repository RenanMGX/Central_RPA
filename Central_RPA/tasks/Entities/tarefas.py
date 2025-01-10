
import subprocess
import re
import string
import random

class Tarefas:
    @property
    def nome(self) -> str:
        return self.__nome_tarefa
    
    @property
    def key(self) -> str:
        return self.__key
    
    @property
    def can_stop(self) -> bool:
        return self.__can_stop
    
    @property
    def permission(self) -> str:
        return self.__permission
    
    @property
    def pk(self):
        return self.__pk
    
    @property
    def nome_para_key(self):
        return self.nome.replace("\\","\\\\")
    
    def __init__(self, *, pk, nome_tarefa:str, permission:str, can_stop:bool=True, infor:str="N/A") -> None:
        self.__nome_tarefa:str = nome_tarefa
        self.__pk = pk
        
        self.__can_stop:bool = can_stop
        self.infor = infor
        self.__permission:str = permission
        
        letters = string.ascii_letters
        self.__key:str = ''.join(random.choice(letters) for _ in range(15))
        
    def __str__(self) -> str:
        return self.nome
    
    def __repr__(self)-> str:
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
        
              
        return "Automação Não Encontrada!"
    
    def executar(self):
        result = subprocess.run(['schtasks', '/run', '/tn', self.nome], capture_output=True, text=True, shell=True)
        print(result)
        return result.stdout

    def encerrar(self):
        if self.__can_stop:
            result = subprocess.run(['schtasks', '/end', '/tn', self.nome], capture_output=True, text=True)
            return result.stdout
        return
    

    @staticmethod
    def all_status():
        saida = subprocess.run(['schtasks', '/query'], capture_output=True, text=True, errors='ignore', encoding='cp850').stdout
        resultado = {}
        pastas = saida.split('\n\n')
        for pasta in pastas:
            caminho = re.search(r'(?<=Pasta: )[\d\D]+?(?=\n)', pasta)
            if caminho:
                caminho = caminho.group()
                if len(caminho) > 1:
                    caminho = caminho[1:]
                else:
                    caminho = ""                    
                pasta = re.sub(r'Pasta:[\d\D]+=', '', pasta)
                for task in pasta.split('\n'):
                    if task:
                        task = re.sub(r'[ ]{2,}', ';', task).split(';')
                        if len(task) == 4:
                            if not "Automações" in caminho:
                                continue
                            resultado[f"{caminho}\\{task[0]}"] = {"status": task[2], "next_execute": task[1]}
        return resultado

