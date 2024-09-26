from django.forms import ModelForm
from . import models

class TarefasForm(ModelForm):
    class Meta:
        model = models.Tarefas
        fields = ['tarefa', 'permission', 'can_stop', 'infor']