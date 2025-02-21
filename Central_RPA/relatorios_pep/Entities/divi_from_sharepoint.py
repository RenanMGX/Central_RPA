import os
import pandas as pd
from copy import deepcopy
import re
from datetime import datetime
from getpass import getuser
from dateutil.relativedelta import relativedelta
from typing import Dict

class StatusFileNotFound(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class LocalStatus:
    @staticmethod
    def find_file(*,path:str, date:datetime):
        if not os.path.exists(path):
            raise FileNotFoundError(f"o caminho {path} não foi encontrado!")
        if not os.path.isdir(path):
            raise TypeError(f"Apenas pastas e não arquivos {path}")
        
        date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        
        folder_per_year = ""
        for folder in os.listdir(path):
            folder = os.path.join(path, folder)
            if os.path.isdir(folder):
                try:
                    if date.year == (datetime.strptime(os.path.basename(folder),"%Y")).year:
                        folder_per_year = folder
                        break
                except:
                    pass
        
        if not folder_per_year:
            raise StatusFileNotFound(f"a pasta {folder_per_year} não foi encontrada")
        elif not os.path.exists(folder_per_year):
            raise StatusFileNotFound(f"a pasta {folder_per_year} não foi encontrada")
        
        arquivos:Dict[datetime, str] = {}
        
        lista_arquivos = os.listdir(folder_per_year)
        lista_arquivos = sorted(lista_arquivos, key=lambda x: os.path.getmtime(os.path.join(folder_per_year, x)))
        
        for file in lista_arquivos:
            file_path = os.path.join(folder_per_year, file)
            if os.path.isfile(file_path):
                try:
                    temp_file_name = re.sub(r"(?<=[0-9]{2}_[0-9]{4})[\d\D]+", "", file)
                    date_file = datetime.strptime(temp_file_name, "%m_%Y")
                
                    while arquivos.get(date_file):
                        try:
                            date_file = date_file + relativedelta(days=1)
                        except:
                            pass
                
                    arquivos[date_file] = file_path
                except:
                    pass
            
        result = ""
        temp_date = deepcopy(date)
        for _ in range(365):
            if temp_date in arquivos:
                result = arquivos.get(temp_date)
                break
            temp_date = temp_date - relativedelta(days=1)
            
        if not result:
            raise StatusFileNotFound("planilha status não foi encontrada")
        
        return result
        

class DiviFromSharepoint:
    def __init__(self, path_statusFile:str, date: datetime) -> None:
        path_statusFile = LocalStatus.find_file(path=path_statusFile, date=date)
        if not os.path.exists(path_statusFile):
            raise FileNotFoundError(f"o arquivo '{path_statusFile}' não foi encontrado!")
        if not path_statusFile.endswith('xlsx'):
            raise TypeError("Apenas arquivos com a extensão '.xlsx'")
        
        self.df_status = pd.read_excel(path_statusFile, sheet_name="Controle", dtype=str , skiprows=7)[['Empresa', 'Divisão', 'Status']]
        self.path_statusFile = path_statusFile
        
    def verificar(self, empresa:str, divisao:str) -> str:
        df = deepcopy(self.df_status)
        
        #import pdb; pdb.set_trace()
        
        result = df[
            (df["Empresa"] == empresa) &
            (df["Divisão"] == divisao)
        ]["Status"]
        
        try:
            del df
        except:
            pass
        
        return result.iloc[0] if not result.empty else ""
    
    def get_lista_divisao(self, status:str) -> list:
        df = deepcopy(self.df_status)
        
        df = df[df["Status"] == status]
        
        if not df.empty:
            return df['Divisão'].unique().tolist() #type:ignore
        return []
        
        
    
if __name__ == "__main__":
    #bot = VerificarStatus(r"R:\Automatizacao_Processo_Comissao\#material\11_2024_status1.xlsx")
    #print(bot.verificar(empresa="P000", divisao="0001"))
    #path = LocalStatus.find_file(path=f'C:\\Users\\{getuser()}\\OneDrive - PATRIMAR ENGENHARIA S A\\Status Liquidação', date=datetime.now())
    plan = DiviFromSharepoint(f'C:\\Users\\{getuser()}\\OneDrive - PATRIMAR ENGENHARIA S A\\Status Liquidação', datetime.now())
    print(plan.get_lista_divisao('Obra em andamento'))
    #import pdb; pdb.set_trace()
    

    