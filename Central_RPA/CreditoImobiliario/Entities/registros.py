import os
import json
from typing import List

class Registros:
    def __init__(self, file_path:str) -> None:
        self.__path = file_path
        if not os.path.exists(self.__path):
            raise FileNotFoundError(f"Path '{self.__path}' not found.")
        if not os.path.basename(self.__path.lower()).endswith('.json'):
            self.__path += '.json'
            
        self.path = self.__path
        
    
    def __save(self, data:dict) -> bool:        
        with open(self.path, 'w', encoding='utf-8') as _file:
            json.dump(data, _file)
        return True
    
    def __register(self, _data):
        data = self.load_all()
        
        _id:int = 0
        if data:
            _id = max([int(x) for x in list(data.keys())]) + 1
        
        data[int(_id)] = _data
        
        self.__save(data)

    def load_all(self) -> dict:
        if os.path.exists(self.path):
            with open(self.path, 'r', encoding='utf-8') as _file:
                return json.load(_file)
        else:
            self.__save({})
            return {}
        
    def loadByIndex(self, _id:int|str) -> dict:
        data = self.load_all()
        
        if str(_id) in data:
            return data[str(_id)]
        else:
            return {}
        
    def delete(self, _id:int|str) -> bool:
        data = self.load_all()
        
        if str(_id) in data:
            del data[str(_id)]
            self.__save(data)
            return True
        else:
            return False
    
    def clear(self) -> bool:
        self.__save({})
        return True
    
    def register_columnsToRemove(self, *, columns:list) -> bool:
        data = {"type": "columnsToRemove", "columns": columns}
        self.__register(data)
        return True
    
    def register_columnsToKeep(self, *, columns:list) -> bool:
        data = {"type": "columnsToKeep", "columns": columns}
        self.__register(data)
        return True
    
    def register_rowsToKeep(self, *, column:str, value_in_rows:list) -> bool:
        data = {"type": "rowsToKeep", "column": column, "value_in_rows": value_in_rows}
        self.__register(data)
        return True
    
    def register_rowsToRemove(self, *, column:str, value_in_rows:list) -> bool:
        data = {"type": "rowsToRemove", "column": column, "value_in_rows": value_in_rows}
        self.__register(data)
        return True
    
    def register_rowsToRemoveByInclude(self, *, column:str, text_include:str) -> bool:
        data = {"type": "rowsToRemoveByInclude", "column": column, "text_include": text_include}
        self.__register(data)
        return True
    

if __name__ == '__main__':
    r = Registros(r'R:\#Prontos\bot_imobme_extraction\json\integraWeb_filtros_empreendimentos.json')
    #r.clear()
    print(r.load_all())
    