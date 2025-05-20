from django.db import models
from rest_framework import serializers

class Permissions(models.Model):
    class Meta:
        permissions = (
            ('log.user', 'Permissão para Usuario Simples'),
            ('log.admin', 'Permissão para Usuario ADMIN'),
        )

class registro(models.Model):
    nome_rpa = models.TextField()
    nome_pc = models.TextField(blank=True, null=True)
    nome_agente = models.TextField(blank=True, null=True)
    status = models.IntegerField()# 0 = Concluido; 1 = Error; 99 = teste
    horario = models.DateTimeField()
    descricao = models.TextField(blank=True, null=True)
    exception = models.TextField(blank=True, null=True)
    ia_analise = models.TextField(blank=True, null=True)
    
    def __str__(self) -> str:
        return self.nome_rpa
    
    
class registroSerializer(serializers.ModelSerializer):
    class Meta:
        model = registro
        fields = '__all__'