from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index_consolidarDadosMultiplasPlanilhas'),
    path('upLoad', views.upload, name='upLoad_consolidarDadosMultiplasPlanilhas'),
    path('setUploadPath', views.set_upload_path, name='setUploadPath_consolidarDadosMultiplasPlanilhas'),
    path('setNameAutomation', views.set_name_automation, name='setNameAutomation_consolidarDadosMultiplasPlanilhas'),
    path('informativo', views.log_informativo, name='informativo_consolidarDadosMultiplasPlanilhas'),
    path('fileDownloadPath', views.file_to_download_path, name='fileDownloadPath_consolidarDadosMultiplasPlanilhas'),
    path('download', views.download_file, name='download_consolidarDadosMultiplasPlanilhas'),
    path('testarAutomacao', views.testar_automacao, name='testarAutomacao_consolidarDadosMultiplasPlanilhas'),
]
