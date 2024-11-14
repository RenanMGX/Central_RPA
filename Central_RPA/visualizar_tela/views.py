from django.core.handlers.wsgi import WSGIRequest #for Typing
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import pyautogui
from io import BytesIO
import base64
from django.contrib.auth.decorators import permission_required, login_required



@login_required()
@permission_required('admin.visu', raise_exception=True) #type: ignore   
def visualizar_tela(request:WSGIRequest):
    return render(request, 'visu.html')

@login_required()
@permission_required('admin.visu', raise_exception=True) #type: ignore   
def atualizar_tela(request:WSGIRequest):
    img_byte = BytesIO()
    pyautogui.screenshot().save(img_byte, format='PNG')
    img_byte = img_byte.getvalue()
    img_byte = base64.b64encode(img_byte).decode('utf-8')
        
    content = {
        "tela_print": img_byte
    }
    return JsonResponse(content)  