from django.db import models

class Uploadpath(models.Model):
    path = models.TextField()

    def __str__(self):
        return self.path
    
class CaminhoAutomacao(models.Model):
    nome = models.TextField()
    
    def __str__(self):
        return self.nome
