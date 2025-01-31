from django.http import JsonResponse, HttpResponseBadRequest
from django.core.handlers.wsgi import WSGIRequest #for Typing
from . import models
from . import forms
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
import json

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def letras(request:WSGIRequest):
    if request.method == 'GET':
        date = request.GET.get('date')
        if date:
            data = models.Letras.objects.filter(data=date)
        else:
            data = models.Letras.objects.all()
            
        if request.GET.get('ambiente'):
            data = data.filter(ambiente=request.GET.get('ambiente'))
            
        if request.GET.get('centro'):
            data = data.filter(centro__icontains=request.GET.get('centro'))
        
        return JsonResponse({'data': list(data.values())})

    elif request.method == 'POST':
        if request.content_type == "application/json":
            dados:dict = json.loads(request.body)

            form = forms.LetrasForm(dados)
            
            if form.is_valid():
                dados = adicionar_letra(dados)
                if dados.get('error'):
                    return HttpResponseBadRequest(dados.get('error'))
                form = forms.LetrasForm(dados)
                form.save()
                return JsonResponse(dados.get('centro'), safe=False)
            else:
                return JsonResponse({'status': 'error', 'errors': form.errors})
            
    elif request.method == 'DELETE':
        pk = request.GET.get('pk')

        if pk:
            item = models.Letras.objects.get(pk=pk)
            item.delete()
            return JsonResponse({'status': 'ok', 'deleted': pk})
        else:
            return HttpResponseBadRequest("header 'pk' não encontrado")

def adicionar_letra(dados:dict) -> dict:   
    range_letras = [chr(101 + num) for num in range(22)] #22
    range_letras.reverse()

    atribuiu = False
    for letra in range_letras:
        if models.Letras.objects.filter(centro=(dados['centro']+letra).upper(), data=dados['data'], ambiente=dados['ambiente']).exists():
            continue
        else:
            dados['centro'] = (dados['centro']+letra).upper()
            atribuiu = True
            break
    
    if atribuiu:
        return dados
    else:
        return {"error": "Não foi encontrado uma letra disponivel para este centro"}
