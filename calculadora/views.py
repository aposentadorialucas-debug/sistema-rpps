from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from clientes.models import Cliente
from datetime import date, timedelta


# ======================================================
# FUNÇÕES AUXILIARES
# ======================================================

def diferenca_dias(data_inicio):
    if not data_inicio:
        return 0
    return (date.today() - data_inicio).days


def converter_dias(dias):
    anos = dias // 365
    resto = dias % 365
    return f"{anos} anos e {resto} dias"


def data_prevista(dias_faltando):
    if dias_faltando <= 0:
        return "Já cumprido"
    return date.today() + timedelta(days=dias_faltando)


# ======================================================
# LISTA DE CLIENTES PARA CÁLCULO
# ======================================================

@login_required
def lista_para_calculo(request):

    clientes = Cliente.objects.all().order_by("nome")

    return render(request, 'calculadora/home.html', {
        'clientes': clientes
    })


# ======================================================
# CÁLCULO DE APOSENTADORIA
# ======================================================

@login_required
def calcular_aposentadoria(request, cliente_id):

    cliente = get_object_or_404(Cliente, id=cliente_id)

    # =============================
    # SEGURANÇA DE DADOS
    # =============================

    if not cliente.data_nascimento:
        return render(request, 'calculadora/erro.html', {
            'mensagem': 'Cliente sem data de nascimento cadastrada.'
        })

    if not cliente.data_ingresso_servico_publico:
        return render(request, 'calculadora/erro.html', {
            'mensagem': 'Cliente sem data de ingresso no serviço público.'
        })

    # =============================
    # CÁLCULO IDADE E TEMPO
    # =============================

    dias_idade = diferenca_dias(cliente.data_nascimento)
    dias_contrib = diferenca_dias(cliente.data_ingresso_servico_publico)

    anos_idade = dias_idade // 365
    anos_contrib = dias_contrib // 365

    sexo = (cliente.sexo or "").upper()
    cargo = (cliente.cargo_atual or "").lower()

    regras = []

    # =====================================================
    # ART. 40 CF (Regra antiga)
    # =====================================================

    idade_min = 60 if sexo == 'M' else 55
    tempo_min = 35 if sexo == 'M' else 30

    dias_para = max(
        max(0, idade_min * 365 - dias_idade),
        max(0, tempo_min * 365 - dias_contrib)
    )

    regras.append({
        "nome": "Art. 40 CF - Aposentadoria por Tempo",
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
        "nome": "EC 20/1998 - Regra de Transição",
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
        "nome": "EC 41/2003 - Aposentadoria Voluntária",
        "apto": dias_para == 0,
        "falta_dias": converter_dias(dias_para),
        "dias_numero": dias_para,
        "data_prevista": data_prevista(dias_para)
    })


    # =====================================================
    # EC 47/2005 (Pontos)
    # =====================================================

    pontos_min = 95 if sexo == 'M' else 85
    pontos = anos_idade + anos_contrib

    dias_para = max(0, pontos_min - pontos) * 365

    regras.append({
        "nome": "EC 47/2005 - Regra dos Pontos",
        "apto": dias_para == 0,
        "falta_dias": converter_dias(dias_para),
        "dias_numero": dias_para,
        "data_prevista": data_prevista(dias_para)
    })


    # =====================================================
    # EC 88/2015 (Compulsória)
    # =====================================================

    dias_para = max(0, 75 * 365 - dias_idade)

    regras.append({
        "nome": "EC 88/2015 - Aposentadoria Compulsória",
        "apto": dias_para == 0,
        "falta_dias": converter_dias(dias_para),
        "dias_numero": dias_para,
        "data_prevista": data_prevista(dias_para)
    })


    # =====================================================
    # EC 103/2019 - Servidor comum
    # =====================================================

    if cargo == 'servidor':

        idade_min = 65 if sexo == 'M' else 62
        tempo_min = 25

        dias_para = max(
            max(0, idade_min * 365 - dias_idade),
            max(0, tempo_min * 365 - dias_contrib)
        )

        regras.append({
            "nome": "EC 103/2019 - Aposentadoria por Idade",
            "apto": dias_para == 0,
            "falta_dias": converter_dias(dias_para),
            "dias_numero": dias_para,
            "data_prevista": data_prevista(dias_para)
        })


    # =====================================================
    # EC 103/2019 - Professor
    # =====================================================

    if cargo == 'professor':

        idade_min = 60 if sexo == 'M' else 57
        tempo_min = 25

        dias_para = max(
            max(0, idade_min * 365 - dias_idade),
            max(0, tempo_min * 365 - dias_contrib)
        )

        regras.append({
            "nome": "EC 103/2019 - Aposentadoria do Magistério",
            "apto": dias_para == 0,
            "falta_dias": converter_dias(dias_para),
            "dias_numero": dias_para,
            "data_prevista": data_prevista(dias_para)
        })


    # =====================================================
    # POLICIAL CIVIL
    # LC 51/1985 + LC 144/2014
    # =====================================================

    if cargo == 'policial':

        tempo_min = 30 if sexo == 'M' else 25
        idade_min = 55 if sexo == 'M' else 52

        dias_para = max(
            max(0, idade_min * 365 - dias_idade),
            max(0, tempo_min * 365 - dias_contrib)
        )

        regras.append({
            "nome": "LC 51/1985 - Aposentadoria Policial",
            "apto": dias_para == 0,
            "falta_dias": converter_dias(dias_para),
            "dias_numero": dias_para,
            "data_prevista": data_prevista(dias_para)
        })


    # =====================================================
    # ORGANIZAÇÃO DAS REGRAS
    # =====================================================

    regras = sorted(regras, key=lambda x: (not x["apto"], x["dias_numero"]))

    melhor_regra = regras[0] if regras else None


    # =====================================================
    # RETORNO
    # =====================================================

    return render(request, 'calculadora/resultado.html', {
        'cliente': cliente,
        'regras': regras,
        'melhor_regra': melhor_regra,
        'anos_idade': anos_idade,
        'anos_contrib': anos_contrib
    })