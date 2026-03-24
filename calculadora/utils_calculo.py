from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from clientes.models import Cliente
from datetime import date, timedelta


# =====================================================
# FUNÇÕES AUXILIARES
# =====================================================

def calcular_idade(data):

    hoje = date.today()

    idade = hoje.year - data.year

    if (hoje.month, hoje.day) < (data.month, data.day):
        idade -= 1

    return idade


def calcular_tempo(data):

    hoje = date.today()

    tempo = hoje.year - data.year

    if (hoje.month, hoje.day) < (data.month, data.day):
        tempo -= 1

    return tempo


def converter_dias(dias):

    anos = dias // 365
    resto = dias % 365

    return f"{anos} anos e {resto} dias"


def data_prevista(dias):

    if dias <= 0:
        return "Já cumprido"

    return date.today() + timedelta(days=dias)


def montar_regra(nome, requisitos, dias_para, integralidade=False, paridade=False):

    apto = all(r["cumprido"] for r in requisitos)

    return {
        "nome": nome,
        "apto": apto,
        "requisitos": requisitos,
        "falta_dias": converter_dias(dias_para),
        "dias_numero": dias_para,
        "data_prevista": data_prevista(dias_para),
        "integralidade": integralidade,
        "paridade": paridade
    }


# =====================================================
# LISTA CLIENTES
# =====================================================

@login_required
def lista_para_calculo(request):

    clientes = Cliente.objects.all().order_by("nome")

    return render(request, "calculadora/home.html", {
        "clientes": clientes
    })


# =====================================================
# CALCULADORA PRINCIPAL
# =====================================================

@login_required
def calcular_aposentadoria(request, cliente_id):

    cliente = get_object_or_404(Cliente, id=cliente_id)

    if not cliente.data_nascimento:
        return render(request, "calculadora/erro.html", {
            "mensagem": "Cliente sem data de nascimento."
        })

    if not cliente.data_ingresso_servico_publico:
        return render(request, "calculadora/erro.html", {
            "mensagem": "Cliente sem data de ingresso no serviço público."
        })

    idade = calcular_idade(cliente.data_nascimento)

    contribuicao = calcular_tempo(
        cliente.data_ingresso_servico_publico
    )

    sexo = cliente.sexo

    regras = []

    # =====================================================
    # ART 40 ORIGINAL (DIREITO ADQUIRIDO)
    # =====================================================

    idade_min = 60 if sexo == "M" else 55
    tempo_min = 35 if sexo == "M" else 30

    requisitos = [

        {"descricao": "Idade mínima", "cumprido": idade >= idade_min},

        {"descricao": "Tempo contribuição",
         "cumprido": contribuicao >= tempo_min}

    ]

    dias_para = max(0, idade_min - idade) * 365

    regras.append(

        montar_regra(
            "Art. 40 CF (redação original)",
            requisitos,
            dias_para,
            True,
            True
        )

    )

    # =====================================================
    # EC 20/1998
    # =====================================================

    idade_min = 53 if sexo == "M" else 48

    tempo_min = 35 if sexo == "M" else 30

    requisitos = [

        {"descricao": "Idade mínima EC20",
         "cumprido": idade >= idade_min},

        {"descricao": "Tempo contribuição",
         "cumprido": contribuicao >= tempo_min}

    ]

    dias_para = max(0, idade_min - idade) * 365

    regras.append(

        montar_regra(
            "EC 20/1998",
            requisitos,
            dias_para,
            True,
            True
        )

    )

    # =====================================================
    # EC 41/2003
    # =====================================================

    idade_min = 60 if sexo == "M" else 55

    tempo_min = 35 if sexo == "M" else 30

    requisitos = [

        {"descricao": "Idade mínima",
         "cumprido": idade >= idade_min},

        {"descricao": "Tempo contribuição",
         "cumprido": contribuicao >= tempo_min},

        {"descricao": "10 anos serviço público",
         "cumprido": contribuicao >= 10},

        {"descricao": "5 anos cargo",
         "cumprido": cliente.tempo_cargo >= 5},

    ]

    dias_para = max(0, idade_min - idade) * 365

    regras.append(

        montar_regra(
            "EC 41/2003",
            requisitos,
            dias_para
        )

    )

    # =====================================================
    # EC 47/2005 (INTEGRALIDADE)
    # =====================================================

    idade_min = 60 if sexo == "M" else 55

    tempo_min = 35 if sexo == "M" else 30

    requisitos = [

        {"descricao": "Idade mínima",
         "cumprido": idade >= idade_min},

        {"descricao": "Tempo contribuição",
         "cumprido": contribuicao >= tempo_min},

        {"descricao": "25 anos serviço público",
         "cumprido": contribuicao >= 25},

        {"descricao": "15 anos carreira",
         "cumprido": contribuicao >= 15},

        {"descricao": "5 anos cargo",
         "cumprido": cliente.tempo_cargo >= 5},

    ]

    dias_para = max(0, idade_min - idade) * 365

    regras.append(

        montar_regra(
            "EC 47/2005",
            requisitos,
            dias_para,
            True,
            True
        )

    )

    # =====================================================
    # EC 103 REGRA PERMANENTE
    # =====================================================

    idade_min = 65 if sexo == "M" else 62

    requisitos = [

        {"descricao": "Idade mínima",
         "cumprido": idade >= idade_min},

        {"descricao": "25 anos contribuição",
         "cumprido": contribuicao >= 25},

        {"descricao": "10 anos serviço público",
         "cumprido": contribuicao >= 10},

        {"descricao": "5 anos cargo",
         "cumprido": cliente.tempo_cargo >= 5},

    ]

    dias_para = max(0, idade_min - idade) * 365

    regras.append(

        montar_regra(
            "EC 103/2019 - Permanente",
            requisitos,
            dias_para
        )

    )

    # =====================================================
    # TRANSIÇÃO PONTOS
    # =====================================================

    pontos = idade + contribuicao

    pontos_min = 100 if sexo == "M" else 90

    requisitos = [

        {"descricao": "30/35 anos contribuição",
         "cumprido": contribuicao >= (35 if sexo == "M" else 30)},

        {"descricao": "20 anos serviço público",
         "cumprido": contribuicao >= 20},

        {"descricao": "5 anos cargo",
         "cumprido": cliente.tempo_cargo >= 5},

        {"descricao": f"{pontos_min} pontos",
         "cumprido": pontos >= pontos_min},

    ]

    dias_para = max(0, pontos_min - pontos) * 365

    regras.append(

        montar_regra(
            "EC 103 - Transição Pontos",
            requisitos,
            dias_para
        )

    )

    # =====================================================
    # COMPULSÓRIA
    # =====================================================

    requisitos = [

        {"descricao": "75 anos idade",
         "cumprido": idade >= 75}

    ]

    dias_para = max(0, 75 - idade) * 365

    regras.append(

        montar_regra(
            "EC 88/2015 - Compulsória",
            requisitos,
            dias_para
        )

    )

    # =====================================================
    # ORGANIZAÇÃO
    # =====================================================

    regras = sorted(regras, key=lambda x: (not x["apto"], x["dias_numero"]))

    return render(request, "calculadora/resultado.html", {

        "cliente": cliente,
        "regras": regras,
        "idade": idade,
        "tempo_contrib": contribuicao

    })