# Use a imagem base do Python
FROM python:3.11

# Defina o diretório de trabalho no contêiner
WORKDIR /app

# Copie os arquivos do projeto para o contêiner
COPY . /app

# Instale as dependências do projeto
RUN pip install -r requirements.txt

# Exponha a porta 5000
EXPOSE 5000

RUN chown -R www-data:www-data /app

# Defina o comando de inicialização do contêiner
#CMD ["python", "manage.py", "runserver", "0.0.0.0:5000"]
CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:5000", "Central_RPA.wsgi:application"]

