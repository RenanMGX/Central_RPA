from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest #for Typing
from . import models
from django.contrib.auth.decorators import permission_required, login_required
from datetime import datetime


@login_required()
@permission_required('rpa_logs.log.user', raise_exception=True) #type: ignore   
def lista(request:WSGIRequest):
    dados = models.registro.objects.all()
    if request.method == "POST":
        if (value:=request.POST.get('nome_rpa')) != 'todos':
            dados = dados.filter(nome_rpa=value)
        if (value:=request.POST.get('nome_pc')) != 'todos':
            dados = dados.filter(nome_pc=value)
        if (value:=request.POST.get('nome_agente')) != 'todos':
            dados = dados.filter(nome_agente=value)
        if (value:=request.POST.get('status')) != 'todos':
            dados = dados.filter(status=value)
        if (value:=request.POST.get('horario')) != '':
            if value:
                dados = dados.filter(horario__date=datetime.strptime(value, '%Y-%m-%d'))
    
    content = {
        "lista" : dados
    }
    return render(request, "lista.html", content)

@login_required()
@permission_required('rpa_logs.log.user', raise_exception=True) #type: ignore   
def filtro_lista(request: WSGIRequest):
    dados = models.registro.objects.all()
    nome_rpa = list(set([x.nome_rpa for x in dados]))
    nome_pc = list(set([x.nome_pc for x in dados]))
    nome_agente = list(set([x.nome_agente for x in dados]))
    status = list(set([x.status for x in dados]))
    now = datetime.now().strftime("%Y-%m-%d")
    
    content = {
        "nome_rpa" : nome_rpa,
        "nome_pc" : nome_pc,
        "nome_agente" : nome_agente,
        "status" : status,
        "now": now
    }
    return render(request, "filtros_lista.html", content)