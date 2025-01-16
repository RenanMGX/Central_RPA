from django.db import models

class InsumoObraPath(models.Model):
    path = models.TextField()
    def __str__(self) -> str:
        return self.path
