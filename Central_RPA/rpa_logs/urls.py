from django.urls import path
from . import endpoints, views


urlpatterns = [
    path('registrar', endpoints.registro, name='Main'), #type: ignore
    path('', views.lista, name='lista')
]

