from django.urls import path
from . import views

app_name = "contratos"

urlpatterns = [
    path('', views.lista, name='lista'),   # <<< ESTA LINHA FALTAVA
    path('tipos/<int:cliente_id>/', views.tipos_contrato, name='tipos'),
    path('gerar/<int:cliente_id>/<str:tipo>/', views.gerar_contrato, name='gerar'),
]