from django.urls import path
from . import views
from django.http import JsonResponse

urlpatterns = [
    path('', views.index, name="baseEstoque_index"),
    path('upload', views.file, name="baseEstoque_upload")
]
