from django.urls import path
from . import endpoints


urlpatterns = [
    path('registrar', endpoints.registro, name='Main') #type: ignore
]

