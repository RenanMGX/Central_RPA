# Use a imagem base do Python
FROM python:3.11

# Defina o diretório de trabalho no contêiner
WORKDIR /app

# Copie os arquivos do projeto para o contêiner
COPY . /app

# Instale as dependências do projeto
RUN pip install -r requirements.txt

# Exponha a porta 80
EXPOSE 5000

# Defina o comando de inicialização do contêiner
CMD ["python", "manage.py", "runserver", "127.0.0.1:5000"]
#CMD ["python"]