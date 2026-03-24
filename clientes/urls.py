from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path('', views.lista_clientes, name='lista'),
    path('novo/', views.cadastro_cliente, name='novo'),
    path('editar/<int:cliente_id>/', views.editar_cliente, name='editar'),
]