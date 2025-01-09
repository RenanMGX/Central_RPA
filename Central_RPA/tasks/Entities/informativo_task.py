import os
import json
import traceback

class Informativo:
    def __init__(self, path:str) -> None:
        #if not os.path.exists(path):
        #    raise FileNotFoundError("arquivo não encontrado")
        self.__path:str = path
        
    def read(self) -> list:
        result:list = []
        try:
            with open(self.__path, 'r', encoding='utf-8')as _file:
                result = json.load(_file)
            return result
        except Exception as err:
            return [traceback.format_exc()]