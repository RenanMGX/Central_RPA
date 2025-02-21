from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index_relatoriosPep'),
    path('start', views.start, name='start_relatoriosPep'),
    path('adminConfig', views.adminConfig, name='adminConfig_relatoriosPep'),
    path('statusTarefa', views.statusTarefa, name='statusTarefa_relatoriosPep'),
]
