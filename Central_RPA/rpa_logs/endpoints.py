from django.http import HttpResponseBadRequest, HttpResponse, HttpResponseServerError, JsonResponse
from django.core.handlers.wsgi import WSGIRequest #for Typing
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import permission_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from . import models
from . import forms
import json
from Central_RPA.Entities.gemini_ia import GeminiIA
from Central_RPA.Entities.credenciais import Credential

@api_view(['PATCH', 'GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def registro(request:WSGIRequest):
    if request.method == "PATCH":
        return registro_path(request)
    elif request.method == "GET":
        return registro_get(request)
    elif request.method == "DELETE":
        return registro_delete(request)

@permission_required('rpa_logs.log.user', raise_exception=True) #type: ignore   
def registro_get(request: WSGIRequest):
    serializer = models.registroSerializer(models.registro.objects.all(), many=True)
    return JsonResponse(serializer.data, safe=False)

@permission_required('rpa_logs.log.admin', raise_exception=True) #type: ignore    
def registro_delete(request: WSGIRequest):
    pk = request.headers.get('pk')
    if pk:
        item = get_object_or_404(models.registro, pk=pk)
        item.delete()
        return HttpResponse(f"o registro '{pk}: {item}' foi apagado!")
    return HttpResponseBadRequest("header 'pk' não encontrado")

@permission_required('rpa_logs.log.user', raise_exception=True) #type: ignore   
def registro_path(request: WSGIRequest):
    if request.content_type == "application/json":
        dados_request:dict = json.loads(request.body)
        
        if (exeption:=dados_request.get("exception")):
            exeption = exeption.replace("<br>", "\n")
            token = Credential("GeminiIA-Token-Default").load().get("token")
            if token:
                try:
                    ia = GeminiIA(token=token,
                                instructions="""
    Você receberá um traceback de erro em Python.
    Sua tarefa é dividida em duas partes:

    1. Análise:
    Identifique e descreva de forma objetiva e direta qual é o erro apresentado no traceback. Foque na causa principal do problema.

    2. Resolução:
    Sugira uma correção breve e prática para resolver o erro identificado. A sugestão deve ser clara, aplicável e sem explicações adicionais.

    Não se apresente, não explique o que está fazendo e não adicione comentários extras. Apenas forneça a análise e a resolução, de forma direta e concisa.
                                """,
                                temperature=0.2,
                                top_p=0.8,
                                top_k=40,
                                )
                    resposta = ia.perguntar(pergunta=exeption).text
                    dados_request["ia_analise"] = resposta
                except Exception as e:
                    pass
        
        print(dados_request)
        form = forms.RegistroForm(dados_request)
        if form.is_valid():
            form.save()
            return HttpResponse("Registrado!")
        else:
            return  HttpResponseServerError("formulario para o registro não é valido")
    else:
        return HttpResponseBadRequest("é permitido apenas json no body da requisição")

    
    
    
    
    
