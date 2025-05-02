from django.core.handlers.wsgi import WSGIRequest #for Typing
from django.core.exceptions import PermissionDenied
import pyautogui
from io import BytesIO
import base64
from django.urls import reverse
from django.http import HttpResponse, Http404
from django.shortcuts import render
import os
from django.core.files.uploadedfile import InMemoryUploadedFile


class Utils:
    @staticmethod
    def superUser_required(func):
        def wrap(*args, **kwargs):
            request:WSGIRequest = args[0]
            if request.user.is_superuser: #type: ignore
                result = func(*args, **kwargs)
                return result
            raise PermissionDenied
        return wrap
    
    @staticmethod
    def gerateImage():
        img_byte = BytesIO()
        pyautogui.screenshot().save(img_byte, format='PNG')
        img_byte = img_byte.getvalue()
        img_byte = base64.b64encode(img_byte).decode('utf-8')
        
        return img_byte
    
    @staticmethod
    def message_retorno(request, text:str, name_route="baseEstoque_index"):
        try:
            route = reverse(name_route)
            content = {
                'message': text,
                'route': route
            }
            return render(request, 'retorno.html', content)
        except:
            raise Http404(f"rota '{name_route}' não encontrada")
    
    @staticmethod
    def upfile(*, path:str, file:InMemoryUploadedFile, new_name:str=""):
        if not os.path.exists(path):
            os.makedirs(path)
        
        if new_name:
            path = os.path.join(path, new_name)
        else:
            path = os.path.join(path, file.name)
            
        with open(path, 'wb+') as _file:
            for chunk in file.chunks():
                _file.write(chunk)
        
        return path
    
    @staticmethod   
    def download_file(file_path:str):
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/octet-stream")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        raise Http404
