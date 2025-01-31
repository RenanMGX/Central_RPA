from . import models
from django.forms import ModelForm

class LetrasForm(ModelForm):
    class Meta:
        model = models.Letras
        fields = ['data', 'centro', 'ambiente']