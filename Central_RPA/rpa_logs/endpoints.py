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
        form = forms.RegistroForm(dados_request)
        if form.is_valid():
            form.save()
            return HttpResponse("Registrado!")
        else:
            return  HttpResponseServerError("formulario para o registro não é valido")
    else:
        return HttpResponseBadRequest("é permitido apenas json no body da requisição")

    
    
    
    
    
