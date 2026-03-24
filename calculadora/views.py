from django.shortcuts import render, get_object_or_404

from clientes.models import Cliente

from calculadora.motor.calculos import calcular_tempos
from calculadora.motor.motor_aposentadoria import analisar_aposentadoria


def lista_para_calculo(request):

    clientes = Cliente.objects.all().order_by("nome")

    return render(
        request,
        "calculadora/home.html",
        {"clientes": clientes}
    )


def calcular(request, cliente_id):

    cliente = get_object_or_404(Cliente, id=cliente_id)

    tempos = calcular_tempos(cliente)

    regras = analisar_aposentadoria(cliente)

    contexto = {
        "cliente": cliente,
        "tempos": tempos,
        "regras": regras,
    }

    return render(
        request,
        "calculadora/resultado.html",
        contexto
    )