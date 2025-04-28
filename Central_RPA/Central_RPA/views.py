from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest #for Typing
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib import messages
from datetime import datetime
import re
from Entities.send_email import SendEmail
from Entities.credenciais import Credential
from Central_RPA.utils import Utils
import os
from django.http import HttpResponse, Http404

@login_required()
def index(request:WSGIRequest):
    return render(request, 'base.html')

def login(request: WSGIRequest):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if not user is None:
            auth_login(request, user)
            if (next:=request.GET.get('next')):
                return redirect(next)
            return redirect('home_index')
        else:
            messages.error(request, 'Usuário ou senha incorretos.')    
    if str(request.user) == "AnonymousUser":
        return render(request, 'registration/login.html')
        
    return redirect('home_index')

@login_required()
def create_user(request:WSGIRequest):
    if request.user.is_superuser: # type: ignore
        return render(request, 'create_user.html')
    
    print(f"o user {request.user} não pode acessar esta pagina")
    return redirect('home_index')

@login_required()
def create_user_action(request:WSGIRequest):
    if request.user.is_superuser: # type: ignore
        if (email:=request.POST.get('email')):
            user_name = email.split('@')[0]
            password = datetime.now().strftime('patrimar#%Y')
            
            if User.objects.filter(email=email).exists():
                return Utils.message_retorno(request, "Erro 01: Usuário já existe", name_route='create_user')
            
            if User.objects.filter(username=user_name).exists():
                last_char = user_name[-1]
                try:
                   last_char = int(last_char)
                   last_char += 1
                   user_name += str(last_char) 
                except:
                    user_name += "1"
                    
            try:
                user = User.objects.create_user(username=user_name, email=email, password=password)
                if "." in user_name:
                    user.first_name = user_name.split(".")[0].title()
                    user.last_name = user_name.split(".")[1].title()
                else:
                    user.first_name = user_name.title()
                
                user.save()
            except Exception as err:
                Utils.message_retorno(request, f"Error2: {str(err)}", name_route='create_user')
                
            try:
                crd:dict = Credential("Microsoft-RPA").load()
                SendEmail(username=crd['email'], password=crd['password'])\
                .mensagem(Destino=email, Assunto="Informações de Acesso ao Sistema RPA", Corpo_email=f"""
Bem-vindo à nossa equipe! Seu usuário foi criado com sucesso. Seguem abaixo as informações de acesso:

Login: {user_name}
Senha: {password}
Link de Acesso: http://patrimar-rpa/

Por favor, acesse o link acima e faça login com as credenciais fornecidas. Recomendamos que você altere sua senha na primeira vez que acessar o sistema para garantir a segurança da sua conta.

Se tiver alguma dúvida ou precisar de assistência, não hesite em entrar em contato conosco pelo email renan.oliveira@patrimar.com.br.

Favor não responder a este email.

Atenciosamente,
""").send()
            except Exception as err:
                Utils.message_retorno(request, f"Error3: {str(err)}", name_route='create_user')
    return Utils.message_retorno(request, "Usuário criado com sucesso", name_route='create_user')


class AlterarSenha(PasswordChangeView):
    template_name = 'alterar_senha.html'
    success_url = reverse_lazy('home_index')

    def form_valid(self, form):
        messages.success(self.request, 'Sua senha foi alterada com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, f'Ocorreu um erro ao tentar alterar a senha. Verifique os campos abaixo.')
        return super().form_invalid(form)
    
@login_required()
def download_file_all(request: WSGIRequest):
    if request.method == "GET":
        file_path = request.GET.get('path')
        if file_path:
            if os.path.exists(file_path):
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(fh.read(), content_type="application/octet-stream")
                    response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                    return response
            raise Http404
    return redirect('home_index')
