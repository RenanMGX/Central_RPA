from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='insumosObras_index'),
    path('delete', views.delete, name='insumosObras_delete'),
    path('create/<str:folder>', views.create, name='insumosObras_create'),
    path('alterPath', views.set_path, name='insumosObras_alterPath'),
    path('status', views.status, name='insumosObras_status'),
    path('start', views.start, name='insumosObras_start'),
    path('download', views.download_file, name='insumosObras_download'),
]