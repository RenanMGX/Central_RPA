from django.urls import path
from . import endpoints, views


urlpatterns = [
    path('registrar', endpoints.registro, name='Main'), #type: ignore
    path('', views.filtro_lista, name='filtro'),
    path('listar', views.lista, name="listar")
]

