from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from clientes.models import Cliente
from datetime import date, timedelta

@login_required
# =============================
# FUNÇÕES AUXILIARES
# =============================

def diferenca_dias(data_inicio):
    return (date.today() - data_inicio).days


def converter_dias(dias):
    anos = dias // 365
    resto = dias % 365
    return f"{anos} anos e {resto} dias"


def data_prevista(dias_faltando):
    if dias_faltando <= 0:
        return "Já cumprido"
    return date.today() + timedelta(days=dias_faltando)

# =============================
# LISTA DE CLIENTES PARA CÁLCULO
# =============================
def lista_para_calculo(request):
    clientes = Cliente.objects.all()
    return render(request, 'calculadora/home.html', {
        'clientes': clientes
    })

def calcular_aposentadoria(request, id):

    cliente = get_object_or_404(Cliente, id=id)

    hoje = date.today()
    dias_idade = diferenca_dias(cliente.data_nascimento)

    if cliente.data_ingresso_servico_publico:
        dias_contrib = diferenca_dias(cliente.data_ingresso_servico_publico)
    else:
        dias_contrib = 0

    anos_idade = dias_idade // 365
    anos_contrib = dias_contrib // 365

    sexo = cliente.sexo
    cargo = cliente.cargo_atual

    regras = []

    # =====================================================
    # ART. 40 CF (Redação pré EC 20)
    # =====================================================
    idade_min = 60 if sexo == 'M' else 55
    tempo_min = 35 if sexo == 'M' else 30

    dias_para = max(
        max(0, idade_min * 365 - dias_idade),
        max(0, tempo_min * 365 - dias_contrib)
    )

    regras.append({
        "nome": "Art. 40 CF - APOSENTADORIA VOLUNTÁRIA POR TEMPO",
        "apto": dias_para == 0,
        "falta_dias": converter_dias(dias_para),
        "dias_numero": dias_para,
        "data_prevista": data_prevista(dias_para)
    })

    # =====================================================
    # EC 20/1998
    # =====================================================
    idade_min = 53 if sexo == 'M' else 48
    tempo_min = 35 if sexo == 'M' else 30

    dias_para = max(
        max(0, idade_min * 365 - dias_idade),
        max(0, tempo_min * 365 - dias_contrib)
    )

    regras.append({
        "nome": "EC 20/1998 - APOSENTADORIA POR IDADE (TRANSIÇÃO)",
        "apto": dias_para == 0,
        "falta_dias": converter_dias(dias_para),
        "dias_numero": dias_para,
        "data_prevista": data_prevista(dias_para)
    })

    # =====================================================
    # EC 41/2003
    # =====================================================
    idade_min = 60 if sexo == 'M' else 55
    tempo_min = 35 if sexo == 'M' else 30

    dias_para = max(
        max(0, idade_min * 365 - dias_idade),
        max(0, tempo_min * 365 - dias_contrib)
    )

    regras.append({
        "nome": "EC 41/2003 - APOSENTADORIA VOLUNTÁRIA",
        "apto": dias_para == 0,
        "falta_dias": converter_dias(dias_para),
        "dias_numero": dias_para,
        "data_prevista": data_prevista(dias_para)
    })

    # =====================================================
    # EC 47/2005 - Pontos 95/85
    # =====================================================
    pontos_min = 95 if sexo == 'M' else 85
    pontos = anos_idade + anos_contrib
    dias_para = max(0, pontos_min - pontos) * 365

    regras.append({
        "nome": "EC 47/2005 - APOSENTADORIA POR PONTOS",
        "apto": dias_para == 0,
        "falta_dias": converter_dias(dias_para),
        "dias_numero": dias_para,
        "data_prevista": data_prevista(dias_para)
    })

    # =====================================================
    # EC 88/2015 - Compulsória
    # =====================================================
    dias_para = max(0, 75 * 365 - dias_idade)

    regras.append({
        "nome": "EC 88/2015 - APOSENTADORIA COMPULSÓRIA",
        "apto": dias_para == 0,
        "falta_dias": converter_dias(dias_para),
        "dias_numero": dias_para,
        "data_prevista": data_prevista(dias_para)
    })

    # =====================================================
    # EC 103/2019 - Servidor
    # =====================================================
    if cargo == 'servidor':

        idade_min = 65 if sexo == 'M' else 62
        tempo_min = 25

        dias_para = max(
            max(0, idade_min * 365 - dias_idade),
            max(0, tempo_min * 365 - dias_contrib)
        )

        regras.append({
            "nome": "EC 103/2019 - APOSENTADORIA POR IDADE",
            "apto": dias_para == 0,
            "falta_dias": converter_dias(dias_para),
            "dias_numero": dias_para,
            "data_prevista": data_prevista(dias_para)
        })

    # =====================================================
    # EC 103/2019 - Magistério
    # =====================================================
    if cargo == 'professor':

        idade_min = 60 if sexo == 'M' else 57
        tempo_min = 25

        dias_para = max(
            max(0, idade_min * 365 - dias_idade),
            max(0, tempo_min * 365 - dias_contrib)
        )

        regras.append({
            "nome": "EC 103/2019 - APOSENTADORIA DO MAGISTÉRIO",
            "apto": dias_para == 0,
            "falta_dias": converter_dias(dias_para),
            "dias_numero": dias_para,
            "data_prevista": data_prevista(dias_para)
        })

    # =====================================================
    # LC 51/1985 + LC 144/2014 - Policial
    # =====================================================
    if cargo == 'militar':

        tempo_min = 30 if sexo == 'M' else 25
        idade_min = 55 if sexo == 'M' else 52

        dias_para = max(
            max(0, idade_min * 365 - dias_idade),
            max(0, tempo_min * 365 - dias_contrib)
        )

        regras.append({
            "nome": "LC 51/1985 c/c LC 144/2014 - APOSENTADORIA POLICIAL",
            "apto": dias_para == 0,
            "falta_dias": converter_dias(dias_para),
            "dias_numero": dias_para,
            "data_prevista": data_prevista(dias_para)
        })

    # =====================================================
    # ORDENAR
    # =====================================================
    regras = sorted(regras, key=lambda x: x["dias_numero"])
    melhor_regra = regras[0] if regras else None

    return render(request, 'calculadora/resultado.html', {
        'cliente': cliente,
        'regras': regras,
        'melhor_regra': melhor_regra,
        'anos_idade': anos_idade,
        'anos_contrib': anos_contrib
    })