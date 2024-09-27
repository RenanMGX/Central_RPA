from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest #for Typing
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib import messages

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



class AlterarSenha(PasswordChangeView):
    template_name = 'alterar_senha.html'
    success_url = reverse_lazy('home_index')

    def form_valid(self, form):
        messages.success(self.request, 'Sua senha foi alterada com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, f'Ocorreu um erro ao tentar alterar a senha. Verifique os campos abaixo.')
        return super().form_invalid(form)
