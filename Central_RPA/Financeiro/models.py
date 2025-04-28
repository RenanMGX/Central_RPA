from django.db import models

class FinanceiroConfig(models.Model):
    """
    Configurações do sistema financeiro
    """
    nome = models.TextField()
    valor = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nome}: {self.valor}"