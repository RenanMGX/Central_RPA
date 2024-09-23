from django.db import models

class Permissions(models.Model):
    class Meta:
        permissions = (
            ('tasks', 'Permissão para acessar a pagina das task permissão obrigatoria'),
            ('tasks.pagamentos_diarios', 'Permissão para acessar a Task de Pagamandos Diarios'),
            ('tasks.atualizar_dashboard', 'Permissão para acessar a Task de Atualização de DashBoard automatica'),
            ('tasks.zenlink', 'Permissão para acessar a Task ddo Conector do app de retenção tecnica com o Zendesk'),
        )


