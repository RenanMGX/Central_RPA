import os
import json

class LogInformativo:
    def __init__(self, path):
        self.path = path
        
    def load(self) -> list:
        if not os.path.exists(self.path):
            return ["caminho do log não encontrado"]
        if os.path.exists(self.path):
            with open(self.path, 'r', encoding='utf-8') as file:
                return json.load(file)
        return []
            
