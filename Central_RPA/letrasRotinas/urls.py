from django.urls import path
from . import endpoints

urlpatterns = [
    path('letras/', endpoints.letras, name='letras'),
]
