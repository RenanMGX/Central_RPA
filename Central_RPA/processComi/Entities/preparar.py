import json
import os
import shutil
from datetime import datetime
import traceback

class Preparar:
    download_path = os.path.join(os.getcwd(), r"processComi\Entities\downloads")
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    
    file_paths = os.path.join(os.getcwd(), r"processComi\Entities\scripts.txt")
    if not os.path.exists(file_paths):
        with open(file_paths, 'w', encoding='utf-8')as _file:
            _file.write(r"C:\Projetos\Automatizacao_Processo_Comissao")
    
    with open(file_paths, 'r', encoding='utf-8')as _file:
        script_path = _file.read()
    
    
    @staticmethod
    def verificar_pasta() -> list:
        return [os.path.join(Preparar.download_path, x) for x in os.listdir(Preparar.download_path) if os.path.isfile(os.path.join(Preparar.download_path, x))]
    
    @staticmethod
    def limpar_pasta():
        for file in os.listdir(Preparar.download_path):
            file = os.path.join(Preparar.download_path, file)
            try:
                os.unlink(file)
            except:
                pass
    
    @staticmethod
    def send_param(date:datetime) -> bool:
        if os.path.exists(Preparar.script_path):
            param_file_path = os.path.join(Preparar.script_path, "param.json")
            with open(param_file_path, 'w')as _file:
                json.dump({
                    "date": date.strftime("%d.%m.%Y"), 
                    "path": Preparar.download_path
                }, _file)
            return True
        return False
    