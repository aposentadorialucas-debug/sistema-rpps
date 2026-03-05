from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from clientes.models import Cliente
from datetime import date
@login_required
def dashboard_home(request):
    total_clientes = Cliente.objects.count()

    aptos = 0
    quase_aptos = 0

    hoje = date.today()

    for cliente in Cliente.objects.all():

        # calcular idade
        dias_idade = (hoje - cliente.data_nascimento).days
        anos_idade = dias_idade // 365

        # calcular tempo serviço público
        if cliente.data_ingresso_servico_publico:
            dias_contrib = (hoje - cliente.data_ingresso_servico_publico).days
            anos_contrib = dias_contrib // 365
        else:
            anos_contrib = 0

        sexo = cliente.sexo

        # regra base simples (exemplo EC 103 servidor comum)
        idade_min = 65 if sexo == 'M' else 62
        tempo_min = 25

        falta_idade = max(0, idade_min - anos_idade)
        falta_tempo = max(0, tempo_min - anos_contrib)

        falta_total = max(falta_idade, falta_tempo)

        if falta_total == 0:
            aptos += 1
        elif falta_total <= 2:
            quase_aptos += 1

    return render(request, 'dashboard/home.html', {
        'total_clientes': total_clientes,
        'clientes_aptos': aptos,
        'clientes_quase_aptos': quase_aptos
    })