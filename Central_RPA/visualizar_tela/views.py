from django.core.handlers.wsgi import WSGIRequest #for Typing
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import permission_required, login_required
from Central_RPA.utils import Utils


#@permission_required('admin.visu', raise_exception=True) #type: ignore
@login_required()
@Utils.superUser_required   
def visualizar_tela(request:WSGIRequest):
    content = {
        "tela_print": Utils.gerateImage()
    }
    return render(request, 'visu.html', content)

#@permission_required('admin.visu', raise_exception=True) #type: ignore   
@login_required()
@Utils.superUser_required
def atualizar_tela(request:WSGIRequest):
    content = {
        "tela_print": Utils.gerateImage()
    }
    return JsonResponse(content)  