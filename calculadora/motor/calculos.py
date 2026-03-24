from datetime import date


# ============================
# IDADE
# ============================

def calcular_idade(data):

    hoje = date.today()

    idade = hoje.year - data.year

    if (hoje.month, hoje.day) < (data.month, data.day):
        idade -= 1

    return idade


# ============================
# DIAS PARA ANOS
# ============================

def dias_para_anos(dias):

    if not dias:
        return 0

    return round(dias / 365, 2)


# ============================
# CALCULAR TEMPOS
# ============================

def calcular_tempos(servidor):

    idade = calcular_idade(servidor.data_nascimento)

    contribuicao = dias_para_anos(
        servidor.tempo_contribuicao
    )

    servico_publico = dias_para_anos(
        servidor.tempo_servico_publico_dias
    )

    carreira = dias_para_anos(
        servidor.tempo_carreira
    )

    cargo = dias_para_anos(
        servidor.tempo_cargo
    )

    magisterio = dias_para_anos(
        servidor.tempo_magisterio
    )

    atividade_policial = dias_para_anos(
        servidor.tempo_atividade_policial
    )

    atividade_especial = dias_para_anos(
        servidor.tempo_atividade_especial
    )

    pontos = idade + contribuicao

    return {

        "idade": idade,
        "contribuicao": contribuicao,
        "servico_publico": servico_publico,
        "carreira": carreira,
        "cargo": cargo,

        "magisterio": magisterio,
        "atividade_policial": atividade_policial,
        "atividade_especial": atividade_especial,

        "pontos": pontos

    }