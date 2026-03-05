from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_para_calculo, name='calculadora_home'),
    path('<int:id>/', views.calcular_aposentadoria, name='calcular_aposentadoria'),
]