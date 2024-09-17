from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest #for Typing
from . import models
from django.contrib.auth.decorators import permission_required, login_required

@login_required()
@permission_required('rpa_logs.log.user', raise_exception=True) #type: ignore   
def lista(request:WSGIRequest):
    content = {
        "lista" : models.registro.objects.all()
    }
    return render(request, "lista.html", content)