from django.db import models

class Permissions(models.Model):
    class Meta:
        permissions = (
            ('tasks', 'Permissão para acessar a pagina das task permissão obrigatoria'),
            ('pagamentos_diarios', 'Permissão para acessar a Task de Pagamandos Diarios'),
            ('atualizar_dashboard', 'Permissão para acessar a Task de Atualização de DashBoard automatica'),
            ('zenlink', 'Permissão para acessar a Task ddo Conector do app de retenção tecnica com o Zendesk'),
            ('teste', 'Permissão para acessar o teste do TASKS'),
        )
        
class Tarefas(models.Model):
    tarefa = models.TextField()
    permission = models.TextField()
    can_stop = models.BooleanField(default=True)
    infor = models.TextField(blank=True, null=True)
    
    def __str__(self) -> str:
        return f"{self.tarefa} : {self.permission}"
    
class RegistroExec(models.Model):
    id_usuario = models.IntegerField()
    nome_tarefa = models.TextField()
    data_exec = models.DateTimeField()
