from django.db import models

class Letras(models.Model):
    data = models.DateField()
    centro = models.TextField()
    ambiente = models.TextField()
    
    def __str__(self):
        return f'{self.data} - {self.centro} - {self.ambiente}'
    
    