from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='insumosObras_index'),
    path('delete', views.delete, name='insumosObras_delete'),
    path('create/<str:folder>', views.create, name='insumosObras_create')
]