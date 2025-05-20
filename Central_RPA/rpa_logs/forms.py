from django.forms import ModelForm
from . import models

class RegistroForm(ModelForm):
    class Meta:
        model = models.registro
        fields = ['nome_rpa', 'nome_pc', 'nome_agente', 'status', 'horario', 'descricao', 'exception', 'ia_analise']