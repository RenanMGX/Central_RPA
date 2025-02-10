from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index_consolidarDadosMultiplasPlanilhas'),
    path('upLoad', views.upload, name='upLoad_consolidarDadosMultiplasPlanilhas'),
    path('setUploadPath', views.set_upload_path, name='setUploadPath_consolidarDadosMultiplasPlanilhas'),
    path('informativo', views.log_informativo, name='informativo_consolidarDadosMultiplasPlanilhas'),
]
