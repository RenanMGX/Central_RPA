from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="processComi_index"),
    path('start/', views.start, name="processComi_start"),
    path('status/', views.status, name="processComi_status"),
    path('list_files/', views.list_files, name="processComi_list_files"),
    path('download', views.download_file, name="processComi_download"),
]