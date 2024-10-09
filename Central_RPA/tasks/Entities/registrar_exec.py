from django.core.handlers.wsgi import WSGIRequest #for Typing
from .. import models, forms
from datetime import datetime


def registrar(request:WSGIRequest, *, task:str):
    if (id_user:=request.user.id):# type: ignore
        form = forms.RegistroExecForm({'id_usuario': id_user, 'nome_tarefa': task, 'data_exec':datetime.now()})
        if form.is_valid():
            form.save()