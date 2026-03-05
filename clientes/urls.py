from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_clientes, name='clientes_home'),
    path('cadastro/', views.cadastrar_cliente, name='cadastrar_cliente'),
    path('listar/', views.listar_clientes, name='listar_clientes'),
    path('editar/<int:id>/', views.editar_cliente, name='editar_cliente'),
    path('excluir/<int:id>/', views.excluir_cliente, name='excluir_cliente'),
]