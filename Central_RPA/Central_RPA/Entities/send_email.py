import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

class SendEmail:
    def __init__(self, username:str, password:str) -> None:
        self.__smtp_server = 'smtp-mail.outlook.com'
        self.__smtp_port = 587
        
        self.__username = username
        self.__password = password
        
    def mensagem(
                self, *,
                Destino:str,
                Assunto:str= "",
                Corpo_email:str,
            ):
        
        msg = MIMEMultipart()
        msg['From'] = self.__username
        msg['To'] = Destino
        msg['Subject'] = Assunto
        
        msg.attach(MIMEText(Corpo_email, 'plain'))

        self.__msg = msg
        return self
        
    def Anexo(self, Attachment_path:str):
        try:
            self.__msg
            if not os.path.exists(Attachment_path):
                raise FileNotFoundError(f"Arquivo não encontrado '{Attachment_path}'")
                
            filename = os.path.basename(Attachment_path)
            with open(Attachment_path, 'rb') as _file:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(_file.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename= {filename}')
                    
            self.__msg.attach(part)
            
            return self
        except KeyError:
            raise Exception(f"Crie um corpo de email primeiro usando '.mensagem'")
            
    
    def send(self):
        try:
            self.__msg
            
            with smtplib.SMTP(self.__smtp_server, self.__smtp_port) as server:
                server.starttls()
                server.login(self.__username, self.__password)
                server.sendmail(self.__msg['From'], self.__msg['To'], self.__msg.as_string())
            
            print("Emai enviado")
            del self.__msg
        
        except KeyError:
            print("Crie um corpo para o email primeiro usando '.mensagem'")
        
if __name__ == "__main__":
    pass
    #Exemplo de uso
    # email = Email(username="email que irá enviar", password="senha do email")
    
    # email.mensagem(
    # Destino="Email destino",
    # Assunto="Assunto do Email",
    # Corpo_email="Corpo do email"
    # )
    
    # email.Anexo("caminho do Anexo")
    
    # email.send()
    