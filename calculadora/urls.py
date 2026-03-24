from django.urls import path
from . import views

app_name = "calculadora"

urlpatterns = [

    # página inicial da calculadora
    path(
        "",
        views.lista_para_calculo,
        name="home",
    ),

    # executar cálculo previdenciário do cliente
    path(
        "cliente/<int:cliente_id>/",
        views.calcular,
        name="calcular",
    ),

]