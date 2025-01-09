import subprocess
import re
from typing import List, Dict
import json

class NewTasks:
    @staticmethod
    def get_tasks(pastas:List[str]=[]):
        tasks_groups = {}
        result = subprocess.run(['schtasks', '/query', '/fo', 'LIST'], capture_output=True, text=True, encoding='cp850')
        result = re.sub(r'\nPasta:', r'\n\nPasta:', result.stdout)
        result = result.split('\n\n\n')
        for group in result:
            pasta = re.search(r'Pasta: (.+)', group)
            pasta = re.sub(r'\s{2,}', ' ', pasta.group())
            pasta = re.search(r'(?<=Pasta: )(.+)', pasta)
            
            tasks_groups[pasta.group().replace("\\", ".")] = group.split('\n\n')
        
        if pastas:
            temp_tasks_groups = {}
            for pasta in pastas:
                for key, value in tasks_groups.items():
                    if pasta.lower() in key.lower():
                        temp_tasks_groups[key] = value
            tasks_groups = temp_tasks_groups
        
        return tasks_groups
    
    
    @staticmethod
    def listar_tarefas(pastas:List[str]=[]):
        tasks_groups = NewTasks.get_tasks(pastas)
        
        
        tasks:List[NewTasks] = []
        for key, value in tasks_groups.items():
            for group in value:
                tasks.append(NewTasks(group, pasta=key))
        
        
        return tasks    
    
    @property
    def enderecoTarefa(self):
        result = re.search(r"Nome da tarefa:[\s]+[\D\d]+", self.__value)
        if result:
            result = re.sub(r"[\n][\d\D]+", "", result.group())
            return re.sub(r"Nome da tarefa:[\s]+", "", result)
        return None
    
    @property
    def nome(self):
        if self.enderecoTarefa:
            return self.enderecoTarefa.replace(f"{self.pasta}\\", "")
        return None
    
    @property
    def proxExec(self):
        result = re.search(r"Hora da próxima execução:[\s]+[\D\d]+", self.__newValue())
        if result:
            result = re.sub(r"[\n][\d\D]+", "", result.group())
            return re.sub(r"Hora da próxima execução:[\s]+", "", result)
        return None 
    
    @property
    def ultimaExec(self):
        result = re.search(r"Horário da última execução:[\s]+[\D\d]+", self.__newValue())
        if result:
            result = re.sub(r"[\n][\d\D]+", "", result.group())
            return re.sub(r"Horário da última execução:[\s]+", "", result)
        return None  
    
    @property
    def status(self):
        result = re.search(r"Status:[\s]+[A-z0-9 \\/\w]+", self.__newValue())
        if result:
            return re.sub(r"Status:[\s]+", "", result.group())
        return None 
    
    @property
    def can_stop(self) -> bool|None:
        result = re.search(r"Comentário:[\s]+[\d\D]+(?=\n)", self.__newValue())
        if result:
            result = re.sub(r"[\n][\d\D]+", "", result.group())
            result = re.sub(r"Comentário:[\s]+", "", result)
            if "{{can_stop=False}}".lower() in result.lower():
                return False
            else:
                return True
        return None
    
    @property
    def json_file(self) -> bool|None:
        result = re.search(r"Comentário:[\s]+[\d\D]+(?=\n)", self.__newValue())
        if result:
            result = re.sub(r"[\n][\d\D]+", "", result.group())
            result = re.sub(r"Comentário:[\s]+", "", result)
            result = re.search(r"(?<=<json>)[\d\D]+(?=</json>)", result)
            if result:
                result = result.group().replace("'",'"')
                try:
                    return json.loads(result)
                except:
                    pass            
        return None
    
    @property
    def permission(self) -> bool|None:
        result = re.search(r"Comentário:[\s]+[\d\D]+(?=\n)", self.__newValue())
        if result:
            result = re.sub(r"[\n][\d\D]+", "", result.group())
            result = re.sub(r"Comentário:[\s]+", "", result)
            result = re.search(r"(?<=<permission>)[\d\D]+(?=</permission>)", result)
            if result:
                return result.group()          
        return "admin.add_logentry"
    
    @property
    def propriedades(self) -> dict:
        return {
            "Pasta": self.pasta,
            "Nome": self.nome,
            "Endereço": self.enderecoTarefa,
            "Proxima Execução": self.proxExec,
            "Ultima Execução": self.ultimaExec,
            "Status": self.status,
            "can_stop": self.can_stop,
            "json_file": self.json_file,
            "permission": self.permission
        }
    
    def __init__(self, value:str, *, pasta:str):
        self.__value = value
        self.pasta = pasta.replace(".", "\\")

        
    def __str__(self):
        return f"Tarefa: {self.nome}"
    
    def __repr__(self):
        return f"Tarefa: {self.nome}"
    
    def __newValue(self):
        return subprocess.run(['schtasks', '/query', '/TN', self.enderecoTarefa, '/V', '/FO', 'LIST'], capture_output=True, text=True, encoding='cp850').stdout
    
    def start(self):
        result = subprocess.run(['schtasks', '/run', '/tn', self.enderecoTarefa], capture_output=True, text=True, shell=True, encoding='cp850')
        return result.stderr  
    
    def stop(self):
        if self.can_stop:
            result = subprocess.run(['schtasks', '/end', '/tn', self.enderecoTarefa], capture_output=True, text=True, encoding='cp850')
            return result.stderr
        return "Tarefa não pode ser parada"
                    
if __name__ == "__main__":
    tasks = NewTasks.listar_tarefas(['Automações'])