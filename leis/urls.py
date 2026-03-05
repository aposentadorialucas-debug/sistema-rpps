from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_leis, name='lista_leis'),
]