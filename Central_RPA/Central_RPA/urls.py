"""
URL configuration for Central_RPA project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import logout
from django.shortcuts import redirect
from . import views
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from visualizar_tela import views as visualizar


def sair(request):
    logout(request)
    return redirect('login')
    
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/rpa_logs/', include('rpa_logs.urls')),
    path('rpa_logs/', include('rpa_logs.urls'), name='rpa_logs'),#
    path('tasks/', include('tasks.urls')),
    path('login/', views.login, name="login"),
    path('logout/', sair, name="logout"),
    path('', views.index, name='home_index'),
    #path('alterar_senha', PasswordChangeView.as_view(template_name='alterar_senha.html', success_url=reverse_lazy('home_index')), name='alterar_senha')
    path('alterar_senha', views.AlterarSenha.as_view(), name='alterar_senha'),
    path('create_user/', views.create_user, name='create_user'),
    path('create_user/action', views.create_user_action, name='create_user_action'),
    path('visu/', visualizar.visualizar_tela, name='visu'),
    path('visu_atu/', visualizar.atualizar_tela, name='visu_atu'),
    path('processComi/', include('processComi.urls')),
    path('baseEstoque/', include('baseEstoque.urls')),
    path('insumosObras/', include('insumosObras.urls')),
    path('letrasRotinas/', include('letrasRotinas.urls')),
    path('consolidarDadosMultiplasPlanilhas/', include('consolidar_dados_multiplas_planilhas.urls')),
    path('relatorios_pep/', include('relatorios_pep.urls')),
    path('Financeiro/', include('Financeiro.urls')),
    path('download', views.download_file_all, name='download'),
    path('creditoImobiliario/', include('CreditoImobiliario.urls')),
]
