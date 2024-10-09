from django.forms import ModelForm
from . import models

class TarefasForm(ModelForm):
    class Meta:
        model = models.Tarefas
        fields = ['tarefa', 'permission', 'can_stop', 'infor']
        
class RegistroExecForm(ModelForm):
    class Meta:
        model = models.RegistroExec
        fields = ['id_usuario', 'nome_tarefa', 'data_exec']
        