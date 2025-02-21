from django.db import models

class AdminConfig(models.Model):
    argv = models.TextField()
    value = models.TextField()
    
    def __str__(self):
        return f"{self.argv}: {self.value}"